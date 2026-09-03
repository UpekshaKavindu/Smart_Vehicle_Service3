using DotNetEnv;
using Microsoft.EntityFrameworkCore;
using VehicleServiceManagement.Data;
using VehicleServiceManagement.Services;

var builder = WebApplication.CreateBuilder(args);

Env.Load();

var host = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "localhost";
var db = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "VehicleServiceDb";
var user = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
var password = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "yourpassword";
var connectionString = $"Host={host};Database={db};Username={user};Password={password}";

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddScoped<ICustomerService, CustomerService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddCors(options =>
{
    options.AddPolicy("ReactApp",
        policy =>
        {
            policy.WithOrigins("http://localhost:5173")
                  .AllowAnyHeader()
                  .AllowAnyMethod();
        });
});

var app = builder.Build();

if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("ReactApp");
app.MapControllers();

using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    dbContext.Database.Migrate();
}

app.Run();