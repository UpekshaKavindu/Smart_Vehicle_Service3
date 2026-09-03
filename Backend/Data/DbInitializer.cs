using VehicleServiceManagement.Models;

namespace VehicleServiceManagement.Data
{
    public static class DbInitializer
    {
        public static void Initialize(AppDbContext context)
        {
            // Look for any customers.
            if (context.Customers.Any())
            {
                return;   // DB has been seeded
            }

            var customers = new Customer[]
            {
                new Customer
                {
                    FirstName = "John",
                    LastName = "Doe",
                    Email = "john.doe@example.com",
                    Phone = "+1-555-0101",
                    Address = "123 Main St, Anytown, AN 12345",
                    CreatedAt = DateTime.UtcNow.AddMonths(-6)
                },
                new Customer
                {
                    FirstName = "Jane",
                    LastName = "Smith",
                    Email = "jane.smith@example.com",
                    Phone = "+1-555-0102",
                    Address = "456 Oak Ave, Othertown, OT 67890",
                    CreatedAt = DateTime.UtcNow.AddMonths(-3)
                },
                new Customer
                {
                    FirstName = "Robert",
                    LastName = "Johnson",
                    Email = "robert.johnson@example.com",
                    Phone = "+1-555-0103",
                    Address = "789 Pine Rd, Sometown, ST 11223",
                    CreatedAt = DateTime.UtcNow.AddMonths(-1)
                },
                new Customer
                {
                    FirstName = "Maria",
                    LastName = "Garcia",
                    Email = "maria.garcia@example.com",
                    Phone = "+1-555-0104",
                    Address = "321 Elm Blvd, Anycity, AC 33445",
                    CreatedAt = DateTime.UtcNow.AddDays(-5)
                }
            };

            context.Customers.AddRange(customers);
            context.SaveChanges();
        }
    }
}