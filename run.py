import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",  # Allows external access
        port=8000,       # Default port
        reload=True,     # Auto-reload on code changes
        workers=1        # Number of worker processes
    )
