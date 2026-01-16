import { signOut, getCurrentUserId } from '@/lib/auth';
import { MoonIcon, SunIcon, LogOut } from 'lucide-react';
import { useTheme } from 'next-themes';
import { Button } from '@/components/ui/Button';

export default function Header() {
  const { theme, setTheme } = useTheme();
  const userId = getCurrentUserId();

  const toggleTheme = () => {
    setTheme(theme === 'dark' ? 'light' : 'dark');
  };

  const handleLogout = () => {
    signOut();
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b border-gray-200 dark:border-gray-700 bg-white/80 dark:bg-gray-900/80 backdrop-blur">
      <div className="container flex h-16 items-center justify-between px-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <h1 className="text-xl font-bold text-white">Todo</h1>
          </div>
          {userId && (
            <div className="hidden md:block">
              <span className="text-sm text-gray-600 dark:text-gray-300">
                Welcome, <span className="font-semibold">{userId}</span>
              </span>
            </div>
          )}
        </div>

        <div className="flex items-center gap-3">
          <Button
            variant="ghost"
            size="icon"
            onClick={toggleTheme}
            aria-label="Toggle theme"
            className="rounded-full hover:bg-gray-100 dark:hover:bg-gray-800"
          >
            {theme === 'dark' ? (
              <SunIcon className="h-5 w-5 text-yellow-500" />
            ) : (
              <MoonIcon className="h-5 w-5 text-gray-700" />
            )}
          </Button>

          <Button
            variant="outline"
            size="sm"
            onClick={handleLogout}
            className="flex items-center gap-2 border-gray-300 dark:border-gray-600 hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400"
          >
            <LogOut className="h-4 w-4" />
            <span className="hidden sm:inline-block">Logout</span>
          </Button>
        </div>
      </div>
    </header>
  );
}