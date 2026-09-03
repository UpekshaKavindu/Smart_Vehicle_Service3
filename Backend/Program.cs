using DotNetEnv;
using Microsoft.EntityFrameworkCore;
using VehicleServiceManagement.Data;
using VehicleServiceManagement.Services;

var builder = WebApplication.CreateBuilder(args);

// Load .env only if not in production (Render uses environment variables)
if (!builder.Environment.IsProduction())
{
    Env.Load();
}

// Determine connection string
string? connectionString = null;

// 1. Try Render's DATABASE_URL (automatically provided if you create a PostgreSQL on Render)
var databaseUrl = Environment.GetEnvironmentVariable("DATABASE_URL");
if (!string.IsNullOrEmpty(databaseUrl))
{
    // Parse the postgres:// URL
    var uri = new Uri(databaseUrl);
    var userInfo = uri.UserInfo.Split(':');
    var host = uri.Host;
    var port = uri.Port;
    var database = uri.LocalPath.TrimStart('/');
    var username = userInfo[0];
    var password = userInfo[1];
    connectionString = $"Host={host};Port={port};Database={database};Username={username};Password={password};SSL Mode=Require;Trust Server Certificate=true;";
}
else
{
    // 2. Fallback to .env or appsettings
    var host = Environment.GetEnvironmentVariable("POSTGRES_HOST") ?? "localhost";
    var db = Environment.GetEnvironmentVariable("POSTGRES_DB") ?? "VehicleServiceDb";
    var user = Environment.GetEnvironmentVariable("POSTGRES_USER") ?? "postgres";
    var password = Environment.GetEnvironmentVariable("POSTGRES_PASSWORD") ?? "yourpassword";
    connectionString = $"Host={host};Database={db};Username={user};Password={password}";
}

builder.Services.AddDbContext<AppDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddScoped<ICustomerService, CustomerService>();

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

// CORS - allow any origin (for simplicity)
builder.Services.AddCors(options =>
{
    options.AddPolicy("AllowAll",
        policy =>
        {
            policy.AllowAnyOrigin()
                  .AllowAnyHeader()
                  .AllowAnyMethod();
        });
});

var app = builder.Build();

// Enable Swagger in all environments (optional)
app.UseSwagger();
app.UseSwaggerUI();

app.UseHttpsRedirection();
app.UseCors("AllowAll");
app.MapControllers();

// Apply migrations and seed data
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    dbContext.Database.Migrate();
    DbInitializer.Initialize(dbContext);
}

app.Run();