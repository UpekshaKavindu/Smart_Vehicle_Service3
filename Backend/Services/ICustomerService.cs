using VehicleServiceManagement.DTOs;

namespace VehicleServiceManagement.Services
{
    public interface ICustomerService
    {
        Task<IEnumerable<CustomerDto>> GetAllAsync();
        Task<CustomerDto?> GetByIdAsync(int id);
        Task<CustomerDto> CreateAsync(CustomerCreateDto dto);
        Task<CustomerDto?> UpdateAsync(CustomerUpdateDto dto);
        Task<bool> DeleteAsync(int id);
        Task<IEnumerable<CustomerDto>> SearchAsync(string searchTerm);
    }
}