import { Task } from '@/lib/types';
import TaskCard from './TaskCard';
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs';
import { Skeleton } from '@/components/ui/Skeleton';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Info } from 'lucide-react';

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  error: string | null;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onUpdate: (id: string, updatedTask: Partial<Task>) => void;
}

export default function TaskList({ tasks, loading, error, onToggle, onDelete, onUpdate }: TaskListProps) {
  const pendingTasks = tasks.filter(task => task.status === 'pending');
  const completedTasks = tasks.filter(task => task.status === 'completed');

  if (error) {
    return (
      <Alert variant="destructive">
        <Info className="h-4 w-4" />
        <AlertDescription>{error}</AlertDescription>
      </Alert>
    );
  }

  if (loading) {
    return (
      <div className="space-y-4">
        {[...Array(3)].map((_, i) => (
          <Skeleton key={i} className="h-20 w-full" />
        ))}
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="text-center py-10">
        <div className="mx-auto h-16 w-16 text-muted-foreground">
          <Info className="h-full w-full" />
        </div>
        <h3 className="mt-4 text-lg font-medium">No tasks yet</h3>
        <p className="text-muted-foreground">Add your first task to get started!</p>
      </div>
    );
  }

  return (
    <div className="mt-6">
      <Tabs defaultValue="all" className="w-full">
        <TabsList className="grid w-full grid-cols-3 bg-gray-100 dark:bg-gray-700 p-1 mb-6 rounded-xl">
          <TabsTrigger
            value="all"
            className="data-[state=active]:bg-white data-[state=active]:text-blue-600 dark:data-[state=active]:bg-gray-800 dark:data-[state=active]:text-blue-400 rounded-lg transition-all"
          >
            All ({tasks.length})
          </TabsTrigger>
          <TabsTrigger
            value="pending"
            className="data-[state=active]:bg-white data-[state=active]:text-blue-600 dark:data-[state=active]:bg-gray-800 dark:data-[state=active]:text-blue-400 rounded-lg transition-all"
          >
            Pending ({pendingTasks.length})
          </TabsTrigger>
          <TabsTrigger
            value="completed"
            className="data-[state=active]:bg-white data-[state=active]:text-blue-600 dark:data-[state=active]:bg-gray-800 dark:data-[state=active]:text-blue-400 rounded-lg transition-all"
          >
            Completed ({completedTasks.length})
          </TabsTrigger>
        </TabsList>

        <TabsContent value="all" className="space-y-4 mt-0">
          {tasks.length > 0 ? (
            <div className="grid grid-cols-1 gap-4">
              {tasks.map((task, index) => (
                <div
                  key={task.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <TaskCard
                    task={task}
                    onToggle={onToggle}
                    onDelete={onDelete}
                    onUpdate={onUpdate}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 animate-fade-in">
              <div className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-500">
                <Info className="h-full w-full" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">No tasks yet</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Get started by adding a new task
              </p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="pending" className="space-y-4 mt-0">
          {pendingTasks.length > 0 ? (
            <div className="grid grid-cols-1 gap-4">
              {pendingTasks.map((task, index) => (
                <div
                  key={task.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <TaskCard
                    task={task}
                    onToggle={onToggle}
                    onDelete={onDelete}
                    onUpdate={onUpdate}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 animate-fade-in">
              <div className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-500">
                <Info className="h-full w-full" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">No pending tasks</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Great job! All tasks are completed.
              </p>
            </div>
          )}
        </TabsContent>

        <TabsContent value="completed" className="space-y-4 mt-0">
          {completedTasks.length > 0 ? (
            <div className="grid grid-cols-1 gap-4">
              {completedTasks.map((task, index) => (
                <div
                  key={task.id}
                  className="animate-fade-in"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <TaskCard
                    task={task}
                    onToggle={onToggle}
                    onDelete={onDelete}
                    onUpdate={onUpdate}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12 animate-fade-in">
              <div className="mx-auto h-16 w-16 text-gray-400 dark:text-gray-500">
                <Info className="h-full w-full" />
              </div>
              <h3 className="mt-4 text-lg font-medium text-gray-900 dark:text-white">No completed tasks</h3>
              <p className="text-gray-500 dark:text-gray-400 mt-1">
                Complete some tasks to see them here.
              </p>
            </div>
          )}
        </TabsContent>
      </Tabs>
    </div>
  );
}