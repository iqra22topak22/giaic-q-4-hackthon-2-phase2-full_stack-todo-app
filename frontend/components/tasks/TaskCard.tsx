import { Task } from '@/lib/types';
import { Card, CardContent } from '@/components/ui/Card';
import { Checkbox } from '@/components/ui/checkbox';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/Button';
import { Edit3, Trash2 } from 'lucide-react';
import { useState } from 'react';
import TaskForm from './TaskForm';

interface TaskCardProps {
  task: Task;
  onToggle: (id: string) => void;
  onDelete: (id: string) => void;
  onUpdate: (id: string, updatedTask: Partial<Task>) => void;
}

export default function TaskCard({ task, onToggle, onDelete, onUpdate }: TaskCardProps) {
  const [isEditing, setIsEditing] = useState(false);

  const handleEdit = (updatedTask: Partial<Task>) => {
    onUpdate(task.id, updatedTask);
    setIsEditing(false);
  };

  return (
    <>
      <Card
        role="region"
        aria-labelledby={`task-title-${task.id}`}
        className={`overflow-hidden transition-all duration-300 hover:shadow-lg border-l-4 ${
          task.status === 'completed'
            ? 'border-green-500 bg-gradient-to-r from-green-50/30 to-emerald-50/30 dark:from-green-900/10 dark:to-emerald-900/10'
            : 'border-blue-500 bg-gradient-to-r from-white to-blue-50 dark:from-gray-800 dark:to-gray-800/50'
        }`}
      >
        <CardContent className="p-6">
          <div className="flex items-start gap-4">
            <div className="pt-1">
              <Checkbox
                id={`task-checkbox-${task.id}`}
                checked={task.status === 'completed'}
                onCheckedChange={() => onToggle(task.id)}
                aria-label={`Mark task "${task.title}" as ${task.status === 'completed' ? 'incomplete' : 'complete'}`}
                className={`h-5 w-5 rounded-full transition-all ${
                  task.status === 'completed'
                    ? 'bg-green-500 border-green-500'
                    : 'border-blue-500 bg-white dark:bg-gray-700'
                }`}
              />
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-3 mb-2 flex-wrap">
                <h3
                  id={`task-title-${task.id}`}
                  className={`font-semibold text-lg ${
                    task.status === 'completed'
                      ? 'line-through text-muted-foreground'
                      : 'text-gray-800 dark:text-gray-100'
                  }`}
                >
                  {task.title}
                </h3>
                <Badge
                  variant={task.status === 'completed' ? 'secondary' : 'default'}
                  className={`${
                    task.status === 'completed'
                      ? 'bg-green-100 text-green-800 border-green-200 dark:bg-green-900/30 dark:text-green-300'
                      : 'bg-blue-100 text-blue-800 border-blue-200 dark:bg-blue-900/30 dark:text-blue-300'
                  }`}
                >
                  {task.status === 'completed' ? 'Completed' : 'Pending'}
                </Badge>
              </div>

              {task.description && (
                <p
                  id={`task-desc-${task.id}`}
                  className={`text-gray-600 dark:text-gray-300 mb-3 ${
                    task.status === 'completed' ? 'line-through' : ''
                  }`}
                >
                  {task.description}
                </p>
              )}

              <div
                className="flex flex-wrap items-center justify-between gap-2 text-xs text-gray-500 dark:text-gray-400"
                aria-describedby={`task-desc-${task.id}`}
              >
                <time dateTime={task.createdAt.toISOString()}>
                  Created: {new Date(task.createdAt).toLocaleDateString()} at {new Date(task.createdAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </time>
                <time dateTime={task.updatedAt.toISOString()}>
                  Updated: {new Date(task.updatedAt).toLocaleDateString()} at {new Date(task.updatedAt).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </time>
              </div>
            </div>

            <div className="flex gap-1">
              <Button
                variant="outline"
                size="sm"
                onClick={() => setIsEditing(true)}
                aria-label={`Edit task: ${task.title}`}
                className="border-gray-300 dark:border-gray-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 text-blue-600 dark:text-blue-400 transition-all hover:scale-105"
              >
                <Edit3 className="h-4 w-4" />
              </Button>
              <Button
                variant="outline"
                size="sm"
                onClick={() => onDelete(task.id)}
                aria-label={`Delete task: ${task.title}`}
                className="border-gray-300 dark:border-gray-600 hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 dark:text-red-400 transition-all hover:scale-105"
              >
                <Trash2 className="h-4 w-4" />
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {isEditing && (
        <div className="mt-4 animate-fade-in">
          <TaskForm
            task={task}
            onSave={(updatedTask) => {
              handleEdit(updatedTask);
            }}
            onCancel={() => setIsEditing(false)}
          />
        </div>
      )}
    </>
  );
}