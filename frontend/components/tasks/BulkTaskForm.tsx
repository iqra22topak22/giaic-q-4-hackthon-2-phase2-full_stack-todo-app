import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/Button';
import { Textarea } from '@/components/ui/textarea';
import { useState } from 'react';
import { Task } from '@/lib/types';

interface BulkTaskFormProps {
  isOpen: boolean;
  onClose: () => void;
  onBulkSave: (tasks: Partial<Task>[]) => void;
}

export default function BulkTaskForm({ isOpen, onClose, onBulkSave }: BulkTaskFormProps) {
  const [bulkText, setBulkText] = useState('');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!bulkText.trim()) {
      return;
    }

    // Split the text by newlines and create tasks
    const taskTitles = bulkText.split('\n').filter(title => title.trim() !== '');

    if (taskTitles.length === 0) {
      return;
    }

    // Create task objects from the titles
    const tasks: Partial<Task>[] = taskTitles.map(title => ({
      title: title.trim(),
      description: '',
      status: 'pending'
    }));

    onBulkSave(tasks);
    setBulkText('');
  };

  const handleClose = () => {
    setBulkText('');
    onClose();
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleClose}>
      <DialogContent className="sm:max-w-[600px] bg-white dark:bg-gray-800 rounded-2xl shadow-2xl border-0 overflow-hidden">
        <div className="bg-gradient-to-r from-green-500 to-emerald-600 p-6">
          <DialogHeader className="text-left text-white">
            <DialogTitle className="text-2xl font-bold">
              Add Multiple Tasks
            </DialogTitle>
            <DialogDescription className="text-green-100">
              Enter one task per line to add multiple tasks at once
            </DialogDescription>
          </DialogHeader>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6 p-6">
          <div className="space-y-4">
            <div className="space-y-2">
              <label htmlFor="bulk-tasks" className="text-gray-700 dark:text-gray-300 block font-medium">
                Task List
              </label>
              <Textarea
                id="bulk-tasks"
                value={bulkText}
                onChange={(e) => setBulkText(e.target.value)}
                placeholder={`Enter one task per line\nExample:\nBuy groceries\nComplete project proposal\nSchedule meeting`}
                rows={10}
                className="border-gray-300 dark:border-gray-600 dark:bg-gray-700 dark:text-white rounded-lg focus:ring-2 focus:ring-green-500 focus:border-transparent font-mono transition-all"
              />
              <p className="text-sm text-gray-500 dark:text-gray-400">
                One task per line. Empty lines will be ignored.
              </p>
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
              className="px-6 py-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700 text-white rounded-lg transition-all shadow-md"
            >
              Add {bulkText.split('\n').filter(t => t.trim() !== '').length} Tasks
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}