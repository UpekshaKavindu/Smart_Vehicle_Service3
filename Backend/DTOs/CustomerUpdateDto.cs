using System.ComponentModel.DataAnnotations;

namespace VehicleServiceManagement.DTOs
{
    public class CustomerUpdateDto
    {
        [Required]
        public int Id { get; set; }

        [Required(ErrorMessage = "First name is required")]
        [StringLength(50)]
        public string FirstName { get; set; } = string.Empty;

        [Required(ErrorMessage = "Last name is required")]
        [StringLength(50)]
        public string LastName { get; set; } = string.Empty;

        [Required(ErrorMessage = "Email is required")]
        [EmailAddress]
        public string Email { get; set; } = string.Empty;

        [Required(ErrorMessage = "Phone is required")]
        [Phone]
        public string Phone { get; set; } = string.Empty;

        [Required(ErrorMessage = "Address is required")]
        public string Address { get; set; } = string.Empty;
    }
}