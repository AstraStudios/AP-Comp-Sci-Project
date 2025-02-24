var builder = WebApplication.CreateBuilder(args);
builder.Services.AddCors(options => // enable react
{
    options.AddPolicy("AllowReactApp",
    policy => policy.AllowAnyOrigin().AllowAnyMethod().AllowAnyHeader());
});

// Add services to the container.
// Learn more about configuring Swagger/OpenAPI at https://aka.ms/aspnetcore/swashbuckle
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

var app = builder.Build();

// Configure the HTTP request pipeline.
if (app.Environment.IsDevelopment())
{
    app.UseSwagger();
    app.UseSwaggerUI();
}

app.UseHttpsRedirection();
app.UseCors("AllowReactApp"); // apply the cors policy we did above

app.MapControllers(); // make sure the controllers are mapped

app.Run();