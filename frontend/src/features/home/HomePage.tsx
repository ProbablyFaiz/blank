import { CheckCircle2, Plus, Search } from "lucide-react";
import type React from "react";
import { useEffect, useState } from "react";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Separator } from "@/components/ui/separator";

interface Task {
  id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  createdAt: Date;
}

type FilterType = "all" | "active" | "completed";

const HomePage: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [newTaskDescription, setNewTaskDescription] = useState("");
  const [newTaskPriority, setNewTaskPriority] =
    useState<Task["priority"]>("medium");
  const [filter, setFilter] = useState<FilterType>("all");
  const [searchQuery, setSearchQuery] = useState("");
  const [isAddDialogOpen, setIsAddDialogOpen] = useState(false);

  // Load tasks from localStorage on mount
  useEffect(() => {
    const savedTasks = localStorage.getItem("tasks");
    if (savedTasks) {
      const parsedTasks = JSON.parse(savedTasks).map((task: any) => ({
        ...task,
        createdAt: new Date(task.createdAt),
      }));
      setTasks(parsedTasks);
    }
  }, []);

  // Save tasks to localStorage whenever tasks change
  useEffect(() => {
    localStorage.setItem("tasks", JSON.stringify(tasks));
  }, [tasks]);

  const addTask = () => {
    if (!newTaskTitle.trim()) return;

    const newTask: Task = {
      id: Date.now().toString(),
      title: newTaskTitle.trim(),
      description: newTaskDescription.trim() || undefined,
      completed: false,
      priority: newTaskPriority,
      createdAt: new Date(),
    };

    setTasks([newTask, ...tasks]);
    setNewTaskTitle("");
    setNewTaskDescription("");
    setNewTaskPriority("medium");
    setIsAddDialogOpen(false);
  };

  const toggleTask = (id: string) => {
    setTasks(
      tasks.map((task) =>
        task.id === id ? { ...task, completed: !task.completed } : task,
      ),
    );
  };

  const deleteTask = (id: string) => {
    setTasks(tasks.filter((task) => task.id !== id));
  };

  const clearCompleted = () => {
    setTasks(tasks.filter((task) => !task.completed));
  };

  const filteredTasks = tasks.filter((task) => {
    const matchesFilter =
      filter === "all" ||
      (filter === "active" && !task.completed) ||
      (filter === "completed" && task.completed);

    const matchesSearch =
      task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      task.description?.toLowerCase().includes(searchQuery.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  const getPriorityColor = (priority: Task["priority"]) => {
    switch (priority) {
      case "high":
        return "bg-red-100 text-red-800 dark:bg-red-900/20 dark:text-red-400";
      case "medium":
        return "bg-yellow-100 text-yellow-800 dark:bg-yellow-900/20 dark:text-yellow-400";
      case "low":
        return "bg-green-100 text-green-800 dark:bg-green-900/20 dark:text-green-400";
    }
  };

  const completedCount = tasks.filter((task) => task.completed).length;
  const totalCount = tasks.length;

  return (
    <div className="py-8 px-4 sm:px-6 lg:px-8">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-slate-900 dark:text-white mb-2">
            Task Manager
          </h1>
          <p className="text-lg text-slate-600 dark:text-slate-300">
            Stay organized and get things done
          </p>
          {totalCount > 0 && (
            <div className="flex justify-center gap-2 mt-4">
              <Badge variant="outline">{totalCount} total</Badge>
              <Badge variant="outline">{completedCount} completed</Badge>
              <Badge variant="outline">
                {totalCount - completedCount} remaining
              </Badge>
            </div>
          )}
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-4 w-4" />
            <Input
              placeholder="Search tasks..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="pl-10"
            />
          </div>

          <div className="flex gap-2">
            <Button
              variant={filter === "all" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("all")}
            >
              All
            </Button>
            <Button
              variant={filter === "active" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("active")}
            >
              Active
            </Button>
            <Button
              variant={filter === "completed" ? "default" : "outline"}
              size="sm"
              onClick={() => setFilter("completed")}
            >
              Completed
            </Button>
          </div>

          <Dialog open={isAddDialogOpen} onOpenChange={setIsAddDialogOpen}>
            <DialogTrigger asChild>
              <Button className="group">
                <Plus className="mr-2 h-4 w-4 group-hover:rotate-90 transition-transform" />
                Add Task
              </Button>
            </DialogTrigger>
            <DialogContent>
              <DialogHeader>
                <DialogTitle>Add New Task</DialogTitle>
                <DialogDescription>
                  Create a new task to stay organized.
                </DialogDescription>
              </DialogHeader>
              <div className="space-y-4 pt-4">
                <div>
                  <Input
                    placeholder="Task title"
                    value={newTaskTitle}
                    onChange={(e) => setNewTaskTitle(e.target.value)}
                  />
                </div>
                <div>
                  <Input
                    placeholder="Description (optional)"
                    value={newTaskDescription}
                    onChange={(e) => setNewTaskDescription(e.target.value)}
                  />
                </div>
                <div>
                  <select
                    value={newTaskPriority}
                    onChange={(e) =>
                      setNewTaskPriority(e.target.value as Task["priority"])
                    }
                    className="w-full p-2 border rounded-md dark:bg-slate-800 dark:border-slate-600"
                  >
                    <option value="low">Low Priority</option>
                    <option value="medium">Medium Priority</option>
                    <option value="high">High Priority</option>
                  </select>
                </div>
                <div className="flex gap-2">
                  <Button
                    onClick={addTask}
                    disabled={!newTaskTitle.trim()}
                    className="flex-1"
                  >
                    Add Task
                  </Button>
                  <Button
                    variant="outline"
                    onClick={() => setIsAddDialogOpen(false)}
                  >
                    Cancel
                  </Button>
                </div>
              </div>
            </DialogContent>
          </Dialog>
        </div>

        {/* Tasks List */}
        <div className="space-y-3">
          {filteredTasks.length === 0 ? (
            <Card className="p-8 text-center">
              <div className="text-slate-400 dark:text-slate-500">
                <CheckCircle2 className="h-12 w-12 mx-auto mb-4 opacity-50" />
                <p className="text-lg font-medium mb-2">
                  {tasks.length === 0
                    ? "No tasks yet"
                    : "No tasks match your filter"}
                </p>
                <p className="text-sm">
                  {tasks.length === 0
                    ? "Add your first task to get started!"
                    : "Try adjusting your search or filter"}
                </p>
              </div>
            </Card>
          ) : (
            filteredTasks.map((task) => (
              <Card
                key={task.id}
                className="group hover:shadow-md transition-shadow"
              >
                <CardContent className="p-4">
                  <div className="flex items-start gap-3">
                    <button
                      type="button"
                      onClick={() => toggleTask(task.id)}
                      className={`mt-1 h-5 w-5 rounded-full border-2 flex items-center justify-center transition-colors ${
                        task.completed
                          ? "bg-green-500 border-green-500 text-white"
                          : "border-gray-300 hover:border-green-500"
                      }`}
                    >
                      {task.completed && <CheckCircle2 className="h-3 w-3" />}
                    </button>

                    <div className="flex-1 min-w-0">
                      <div className="flex items-center gap-2 mb-1">
                        <h3
                          className={`font-medium ${
                            task.completed
                              ? "text-slate-500 line-through"
                              : "text-slate-900 dark:text-white"
                          }`}
                        >
                          {task.title}
                        </h3>
                        <Badge className={getPriorityColor(task.priority)}>
                          {task.priority}
                        </Badge>
                      </div>
                      {task.description && (
                        <p
                          className={`text-sm ${
                            task.completed
                              ? "text-slate-400 line-through"
                              : "text-slate-600 dark:text-slate-300"
                          }`}
                        >
                          {task.description}
                        </p>
                      )}
                      <p className="text-xs text-slate-400 mt-1">
                        Created {task.createdAt.toLocaleDateString()}
                      </p>
                    </div>

                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => deleteTask(task.id)}
                      className="opacity-0 group-hover:opacity-100 transition-opacity text-red-500 hover:text-red-700 hover:bg-red-50"
                    >
                      Delete
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))
          )}
        </div>

        {/* Footer Actions */}
        {completedCount > 0 && (
          <div className="mt-6 text-center">
            <Separator className="mb-4" />
            <Button
              variant="outline"
              onClick={clearCompleted}
              className="text-red-500 hover:text-red-700 hover:bg-red-50"
            >
              Clear {completedCount} Completed Task
              {completedCount !== 1 ? "s" : ""}
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};

export default HomePage;
