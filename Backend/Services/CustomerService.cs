using Microsoft.EntityFrameworkCore;
using VehicleServiceManagement.Data;
using VehicleServiceManagement.DTOs;
using VehicleServiceManagement.Models;

namespace VehicleServiceManagement.Services
{
    public class CustomerService : ICustomerService
    {
        private readonly AppDbContext _context;

        public CustomerService(AppDbContext context)
        {
            _context = context;
        }

        public async Task<IEnumerable<CustomerDto>> GetAllAsync()
        {
            return await _context.Customers
                .Select(c => new CustomerDto
                {
                    Id = c.Id,
                    FirstName = c.FirstName,
                    LastName = c.LastName,
                    Email = c.Email,
                    Phone = c.Phone,
                    Address = c.Address,
                    CreatedAt = c.CreatedAt
                })
                .ToListAsync();
        }

        public async Task<CustomerDto?> GetByIdAsync(int id)
        {
            var customer = await _context.Customers.FindAsync(id);
            if (customer == null) return null;
            return new CustomerDto
            {
                Id = customer.Id,
                FirstName = customer.FirstName,
                LastName = customer.LastName,
                Email = customer.Email,
                Phone = customer.Phone,
                Address = customer.Address,
                CreatedAt = customer.CreatedAt
            };
        }

        public async Task<CustomerDto> CreateAsync(CustomerCreateDto dto)
        {
            var exists = await _context.Customers.AnyAsync(c => c.Email == dto.Email);
            if (exists)
                throw new InvalidOperationException("A customer with this email already exists.");

            var customer = new Customer
            {
                FirstName = dto.FirstName,
                LastName = dto.LastName,
                Email = dto.Email,
                Phone = dto.Phone,
                Address = dto.Address,
                CreatedAt = DateTime.UtcNow
            };

            _context.Customers.Add(customer);
            await _context.SaveChangesAsync();

            return new CustomerDto
            {
                Id = customer.Id,
                FirstName = customer.FirstName,
                LastName = customer.LastName,
                Email = customer.Email,
                Phone = customer.Phone,
                Address = customer.Address,
                CreatedAt = customer.CreatedAt
            };
        }

        public async Task<CustomerDto?> UpdateAsync(CustomerUpdateDto dto)
        {
            var customer = await _context.Customers.FindAsync(dto.Id);
            if (customer == null) return null;

            if (customer.Email != dto.Email)
            {
                var exists = await _context.Customers.AnyAsync(c => c.Email == dto.Email && c.Id != dto.Id);
                if (exists)
                    throw new InvalidOperationException("Another customer already uses this email.");
            }

            customer.FirstName = dto.FirstName;
            customer.LastName = dto.LastName;
            customer.Email = dto.Email;
            customer.Phone = dto.Phone;
            customer.Address = dto.Address;

            _context.Entry(customer).State = EntityState.Modified;
            await _context.SaveChangesAsync();

            return new CustomerDto
            {
                Id = customer.Id,
                FirstName = customer.FirstName,
                LastName = customer.LastName,
                Email = customer.Email,
                Phone = customer.Phone,
                Address = customer.Address,
                CreatedAt = customer.CreatedAt
            };
        }

        public async Task<bool> DeleteAsync(int id)
        {
            var customer = await _context.Customers.FindAsync(id);
            if (customer == null) return false;

            _context.Customers.Remove(customer);
            await _context.SaveChangesAsync();
            return true;
        }

        public async Task<IEnumerable<CustomerDto>> SearchAsync(string searchTerm)
        {
            if (string.IsNullOrWhiteSpace(searchTerm))
                return await GetAllAsync();

            searchTerm = searchTerm.ToLower();
            return await _context.Customers
                .Where(c => c.FirstName.ToLower().Contains(searchTerm) ||
                            c.LastName.ToLower().Contains(searchTerm) ||
                            c.Email.ToLower().Contains(searchTerm) ||
                            c.Phone.Contains(searchTerm))
                .Select(c => new CustomerDto
                {
                    Id = c.Id,
                    FirstName = c.FirstName,
                    LastName = c.LastName,
                    Email = c.Email,
                    Phone = c.Phone,
                    Address = c.Address,
                    CreatedAt = c.CreatedAt
                })
                .ToListAsync();
        }
    }
}