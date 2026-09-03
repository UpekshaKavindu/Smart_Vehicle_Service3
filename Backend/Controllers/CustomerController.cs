using Microsoft.AspNetCore.Mvc;
using VehicleServiceManagement.DTOs;
using VehicleServiceManagement.Services;

namespace VehicleServiceManagement.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    public class CustomerController : ControllerBase
    {
        private readonly ICustomerService _customerService;

        public CustomerController(ICustomerService customerService)
        {
            _customerService = customerService;
        }

        [HttpGet]
        public async Task<ActionResult<IEnumerable<CustomerDto>>> GetAll()
        {
            var customers = await _customerService.GetAllAsync();
            return Ok(customers);
        }

        [HttpGet("{id}")]
        public async Task<ActionResult<CustomerDto>> GetById(int id)
        {
            var customer = await _customerService.GetByIdAsync(id);
            if (customer == null)
                return NotFound($"Customer with ID {id} not found.");
            return Ok(customer);
        }

        [HttpGet("search")]
        public async Task<ActionResult<IEnumerable<CustomerDto>>> Search([FromQuery] string q)
        {
            var results = await _customerService.SearchAsync(q);
            return Ok(results);
        }

        [HttpPost]
        public async Task<ActionResult<CustomerDto>> Create([FromBody] CustomerCreateDto dto)
        {
            try
            {
                var created = await _customerService.CreateAsync(dto);
                return CreatedAtAction(nameof(GetById), new { id = created.Id }, created);
            }
            catch (InvalidOperationException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (Exception)
            {
                return StatusCode(500, "An error occurred while creating the customer.");
            }
        }

        [HttpPut("{id}")]
        public async Task<ActionResult<CustomerDto>> Update(int id, [FromBody] CustomerUpdateDto dto)
        {
            if (id != dto.Id)
                return BadRequest("ID mismatch.");

            try
            {
                var updated = await _customerService.UpdateAsync(dto);
                if (updated == null)
                    return NotFound($"Customer with ID {id} not found.");
                return Ok(updated);
            }
            catch (InvalidOperationException ex)
            {
                return BadRequest(new { error = ex.Message });
            }
            catch (Exception)
            {
                return StatusCode(500, "An error occurred while updating the customer.");
            }
        }

        [HttpDelete("{id}")]
        public async Task<IActionResult> Delete(int id)
        {
            var deleted = await _customerService.DeleteAsync(id);
            if (!deleted)
                return NotFound($"Customer with ID {id} not found.");
            return NoContent();
        }
    }
}