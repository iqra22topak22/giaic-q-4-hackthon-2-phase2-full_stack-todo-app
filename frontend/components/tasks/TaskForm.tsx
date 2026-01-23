import { Task } from '@/lib/types';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/Button';
import { Input } from '@/components/ui/Input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { useState, useEffect } from 'react';

interface TaskFormProps {
  task?: Task;
  onSave: (task: Partial<Task>) => void;
  onCancel: () => void;
}

export default function TaskForm({ task, onSave, onCancel }: TaskFormProps) {
  const [title, setTitle] = useState(task?.title || '');
  const [description, setDescription] = useState(task?.description || '');
  const [status, setStatus] = useState<'pending' | 'completed'>(task?.status || 'pending');
  const [isOpen, setIsOpen] = useState(!!task); // Open dialog if editing

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description || '');
      setStatus(task.status);
      setIsOpen(true);
    }
  }, [task]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!title.trim()) {
      return;
    }

    onSave({
      title: title.trim(),
      description: description.trim(),
      status
    });

    // Don't reset form here since parent will handle closing
  };

  const resetForm = () => {
    setTitle('');
    setDescription('');
    setStatus('pending');
    setIsOpen(false);
  };

  const handleClose = () => {
    resetForm();
    onCancel();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[500px] bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border-0 overflow-hidden">
        <div className={`bg-gradient-to-r ${task ? 'from-purple-500 to-indigo-600' : 'from-blue-500 to-indigo-600'} p-6`}>
          <DialogHeader className="text-left text-white">
            <DialogTitle className="text-2xl font-bold">
              {task ? 'Edit Task' : 'Add New Task'}
            </DialogTitle>
            <DialogDescription className="text-blue-100">
              {task ? 'Update your task details' : 'Fill in the details for your new task'}
            </DialogDescription>
          </DialogHeader>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 p-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title" className="text-gray-700 dark:text-gray-300 font-medium">
                Title *
              </Label>
              <Input
                id="title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Enter task title"
                required
                className="py-3 px-4 border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div className="space-y-2">
              <Label htmlFor="description" className="text-gray-700 dark:text-gray-300 font-medium">
                Description
              </Label>
              <Textarea
                id="description"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                placeholder="Enter task description (optional)"
                rows={4}
                className="border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              />
            </div>

            <div className="space-y-2">
              <Label className="text-gray-700 dark:text-gray-300 font-medium">Status</Label>
              <div className="flex space-x-6">
                <div className="flex items-center space-x-3">
                  <input
                    type="radio"
                    id="pending"
                    name="status"
                    checked={status === 'pending'}
                    onChange={() => setStatus('pending')}
                    className="h-5 w-5 text-blue-600 focus:ring-blue-500"
                  />
                  <Label htmlFor="pending" className="text-gray-700 dark:text-gray-300 cursor-pointer font-medium">
                    Pending
                  </Label>
                </div>
                <div className="flex items-center space-x-3">
                  <input
                    type="radio"
                    id="completed"
                    name="status"
                    checked={status === 'completed'}
                    onChange={() => setStatus('completed')}
                    className="h-5 w-5 text-blue-600 focus:ring-blue-500"
                  />
                  <Label htmlFor="completed" className="text-gray-700 dark:text-gray-300 cursor-pointer font-medium">
                    Completed
                  </Label>
                </div>
              </div>
            </div>
          </div>

          <DialogFooter className="flex sm:justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
            <Button
              type="button"
              variant="outline"
              onClick={handleClose}
              className="px-6 py-2 border-gray-300 dark:border-gray-600 hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 transition-all"
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="px-6 py-2 bg-gradient-to-r from-blue-500 to-indigo-600 hover:from-blue-600 hover:to-indigo-700 text-white rounded-lg transition-all shadow-md"
            >
              {task ? 'Update Task' : 'Add Task'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}