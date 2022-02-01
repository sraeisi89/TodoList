import sys
import sqlite3 #for storing data

class Task:
    #constructor
    def __init__(self):
        self.conn = sqlite3.connect("todo.db")
        self.cursor = self.conn.cursor()

        self.ID = 0
        self.Description = ""
        self.IsCompleted = ""

    def Save(self):
        # Create table if not exists
        self.cursor.execute("CREATE TABLE IF NOT EXISTS Tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, description TEXT, isCompleted TEXT)")
        #insert new row to db
        self.cursor.execute("INSERT INTO Tasks (description, isCompleted) VALUES ('" + self.Description + "','" + self.IsCompleted + "')")
        self.conn.commit()
        self.conn.close()

    def PrintAllTasks(self):
        try:
            c = self.cursor.execute("SELECT * from Tasks")
            tasks = c.fetchall()
            if len(tasks) == 0:
                print("No todos for today!!")
            for t in tasks:
                # id - description
                print(t[0], "-", t[1], "[", t[2], "]")
        except:
            print("No todos for today!!")



    def RemoveTask(self):
        try:
            i = self.cursor.execute("SELECT id From Tasks Where id =" + str(self.ID))
            print(i.fetchone())
            if not i.fetchone():
                print ("Task does not exist")
            else:
                self.cursor.execute("DELETE FROM Tasks WHERE id = " + str(self.ID))
                self.conn.commit()
                self.conn.close()
        except:
            print("No todos to remove!!")

    def CheckTask(self):
        try:
            i = self.cursor.execute("SELECT id From Tasks Where id =" + str(self.ID))
            if not i.fetchone():
                print("Task does not exist")
            else:
                self.cursor.execute("UPDATE Tasks SET isCompleted = 'X' WHERE id = " + str(self.ID))
                self.conn.commit()
                self.conn.close()
        except:
            print("No todos to check!!")


if __name__ == "__main__":
    taskType = ""
    taskParameter = ""
    if len(sys.argv) == 1:
        print("\nCommand Line Todo application"
              "\n\n========================= \n\nCommand line arguments: \n"
              " -l   Lists all the tasks \n -a   Adds a new task \n"
              " -r   Removes a task \n -c   Completes a task")
        print("\n>>>>please enter an argument<<<<")
        quit()

    #if program executed with 1 arguments
    if len(sys.argv) > 1:
        taskType = sys.argv[1]

    #if program executed with 2 arguments
    if len(sys.argv) > 2:
        taskParameter = sys.argv[2]


    #add task
    if taskType == "-a":
        if not taskParameter:
            print("Unable to add: no task provided")
        else:
            task = Task()
            task.IsCompleted = ""
            task.Description = taskParameter
            task.Save()

    #list all tasks
    elif taskType == "-l":
        task = Task()
        task.PrintAllTasks()

    #remove task
    elif taskType == "-r":
        if not taskParameter:
            print("Unable to remove: no index provided")
        elif not taskParameter.isnumeric():
            print("Unable to remove: index is not a number")
        else:
            task = Task()
            task.ID = int(taskParameter)
            task.RemoveTask()

    #complete
    elif taskType == "-c":
        if not taskParameter:
            print("Unable to check: no index provided")
        elif not taskParameter.isnumeric():
            print("Unable to check: index is not a number")
        else:
            task = Task()
            task.ID = int(taskParameter)
            task.CheckTask()

    else:
        print("Unsupported argument : " + taskType)



