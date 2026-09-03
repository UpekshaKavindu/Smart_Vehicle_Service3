using DotNetEnv;
using Microsoft.EntityFrameworkCore;
using VehicleServiceManagement.Data;
using VehicleServiceManagement.Services;

var builder = WebApplication.CreateBuilder(args);

if (!builder.Environment.IsProduction())
{
    Env.Load();
}

string? connectionString = null;
var databaseUrl = Environment.GetEnvironmentVariable("DATABASE_URL");
if (!string.IsNullOrEmpty(databaseUrl))
{
    var uri = new Uri(databaseUrl);
    var userInfo = uri.UserInfo.Split(':');
    var host = uri.Host;
    var port = uri.Port == -1 ? 5432 : uri.Port;
    var database = uri.LocalPath.TrimStart('/');
    var username = userInfo[0];
    var password = userInfo[1];
    connectionString = $"Host={host};Port={port};Database={database};Username={username};Password={password};SSL Mode=Require;Trust Server Certificate=true;";
}
else
{
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

app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();
app.UseCors("AllowAll");
app.MapControllers();

using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<AppDbContext>();
    dbContext.Database.Migrate();
    DbInitializer.Initialize(dbContext);
}

app.Run();