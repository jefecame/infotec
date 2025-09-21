# =============================================================================
# INFOTEC - Fix Laravel Storage Directories (Windows PowerShell)
# =============================================================================
# PURPOSE: Fix "Please provide a valid cache path" error in Codespaces/Windows
# USAGE: .\scripts\Fix-StoragePermissions.ps1
# =============================================================================

Write-Host "🔧 INFOTEC - Fixing Laravel Storage Directories" -ForegroundColor Green

# Define the Laravel source directory
$LaravelDir = ".\src"

if (-not (Test-Path $LaravelDir)) {
    Write-Host "❌ Laravel directory not found. Expected: $LaravelDir" -ForegroundColor Red
    exit 1
}

Set-Location $LaravelDir
Write-Host "📁 Working directory: $(Get-Location)" -ForegroundColor Cyan

# =============================================================================
# CREATE REQUIRED STORAGE DIRECTORIES
# =============================================================================

Write-Host "📁 Creating storage directory structure..." -ForegroundColor Yellow

# Create all required storage directories
$RequiredDirs = @(
    "storage\framework\cache",
    "storage\framework\cache\data",
    "storage\framework\sessions",
    "storage\framework\testing",
    "storage\framework\views",
    "storage\logs",
    "storage\app\private",
    "storage\app\public",
    "bootstrap\cache"
)

foreach ($dir in $RequiredDirs) {
    if (-not (Test-Path $dir)) {
        New-Item -ItemType Directory -Path $dir -Force | Out-Null
        Write-Host "   ✅ Created: $dir" -ForegroundColor Green
    } else {
        Write-Host "   ✓ Exists: $dir" -ForegroundColor Gray
    }
}

# Create .gitignore files to preserve directory structure
$GitIgnoreDirs = @(
    "storage\framework\cache\data",
    "storage\framework\sessions",
    "storage\framework\testing",
    "storage\framework\views",
    "storage\logs",
    "storage\app\private",
    "storage\app\public",
    "bootstrap\cache"
)

foreach ($dir in $GitIgnoreDirs) {
    $gitIgnoreFile = Join-Path $dir ".gitignore"
    if (-not (Test-Path $gitIgnoreFile)) {
        @"
*
!.gitignore
"@ | Out-File -FilePath $gitIgnoreFile -Encoding UTF8
    }
}

Write-Host "✅ Storage directories created successfully" -ForegroundColor Green

# =============================================================================
# VERIFY STRUCTURE
# =============================================================================

Write-Host "🔍 Verifying directory structure..." -ForegroundColor Yellow

$MissingDirs = @()

foreach ($dir in $RequiredDirs) {
    if (-not (Test-Path $dir)) {
        $MissingDirs += $dir
    }
}

if ($MissingDirs.Count -eq 0) {
    Write-Host "✅ All required directories exist" -ForegroundColor Green
} else {
    Write-Host "❌ Missing directories:" -ForegroundColor Red
    foreach ($dir in $MissingDirs) {
        Write-Host "   - $dir" -ForegroundColor Red
    }
    exit 1
}

# =============================================================================
# TEST CACHE FUNCTIONALITY
# =============================================================================

Write-Host "🧪 Testing cache functionality..." -ForegroundColor Yellow

# Test if we can write to cache directory
$TestFile = "storage\framework\cache\data\test_write_permission"
try {
    "test" | Out-File -FilePath $TestFile -Encoding UTF8
    Remove-Item $TestFile -Force
    Write-Host "✅ Cache directory is writable" -ForegroundColor Green
} catch {
    Write-Host "❌ Cache directory is not writable: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

# Test views directory
$TestFile = "storage\framework\views\test_write_permission"
try {
    "test" | Out-File -FilePath $TestFile -Encoding UTF8
    Remove-Item $TestFile -Force
    Write-Host "✅ Views directory is writable" -ForegroundColor Green
} catch {
    Write-Host "❌ Views directory is not writable: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}

Write-Host "🎉 Storage directories fixed successfully!" -ForegroundColor Green
Write-Host "💡 Laravel cache should now work properly" -ForegroundColor Cyan

# Clear any existing cache if artisan is available
if (Test-Path "artisan") {
    Write-Host "🧹 Clearing existing cache..." -ForegroundColor Yellow
    try {
        & php artisan config:clear 2>$null
        & php artisan cache:clear 2>$null
        & php artisan view:clear 2>$null
        Write-Host "✅ Cache cleared" -ForegroundColor Green
    } catch {
        Write-Host "⚠️ Could not clear cache (this is normal if Laravel isn't fully set up yet)" -ForegroundColor Yellow
    }
}

Write-Host "✨ Fix completed successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Run: docker compose up -d" -ForegroundColor White
Write-Host "   2. Wait for containers to start" -ForegroundColor White
Write-Host "   3. Access: http://localhost:8000" -ForegroundColor White