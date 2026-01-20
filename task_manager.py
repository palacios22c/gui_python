'''
Task manager using NiceGUI

Users can add tasks with priorities and optional notes.
Tasks can be completed, edited, or deleted at any time.
The list automatically sorts by priority and updates dynamically.
A light/dark mode toggle and a live counter enhance usability.
'''

# Module
from nicegui import ui, app

# Tasks as dict

tasks: list[dict] = []

# Functions
def priority_value(priority: str) -> int:
    """Return numeric priority value for sorting."""
    return {'high': 3, 'normal': 2, 'low': 1}[priority]

def sort_tasks() -> None:
    """Sort tasks by priority (descending)."""
    tasks.sort(key=lambda t: priority_value(t['priority']), reverse=True)

def pending_tasks_count() -> int:
    """Return the number of pending tasks."""
    return sum(1 for task in tasks if not task['completed'])

# Update functions
def update_title() -> None:
    """Update the main title with pending tasks count."""
    title.set_text(f'Task List ({pending_tasks_count()} pending)')

def update_task_list() -> None:
    """Re-render the task list."""
    sort_tasks()
    tasks_container.clear()

    # Colors
    priority_colors = {
        'low': 'text-green-600',
        'normal': 'text-yellow-600',
        'high': 'text-red-600',
    }

    with tasks_container:
        for task in tasks:
            color = priority_colors[task['priority']]

            with ui.row().classes('items-center gap-4'):
                ui.checkbox(
                    value=task['completed'],
                    on_change=lambda e, t=task: toggle_task(t, e.value)
                )

                ui.label(task['text']).classes(
                    f"{'line-through text-gray-500' if task['completed'] else color}"
                )

                ui.label(f"[{task['priority'].capitalize()}]").classes(color)

                if task['notes']:
                    ui.label(f"({task['notes']})").classes('text-gray-400 italic')

                ui.button(
                    'Edit',
                    on_click=lambda _, t=task: open_edit_dialog(t)
                ).classes('bg-yellow-500 text-white px-3 py-1 rounded')

                ui.button(
                    'Delete',
                    on_click=lambda _, t=task: delete_task(t)
                ).classes('bg-red-500 text-white px-3 py-1 rounded')

    update_title()

# Task actions
def add_task() -> None:
    """Add a new task"""
    text = task_input.value.strip()
    priority = priority_selector.value
    notes = notes_input.value.strip()

    if not text:
        return

    tasks.append({
        'text': text,
        'completed': False,
        'priority': priority,
        'notes': notes if notes else None,
    })

    task_input.value = ''
    notes_input.value = ''
    priority_selector.value = 'low'

    update_task_list()

def toggle_task(task: dict, completed: bool) -> None:
    """Mark a task as completed or not"""
    task['completed'] = completed
    update_task_list()

def delete_task(task: dict) -> None:
    """Delete a task"""
    tasks.remove(task)
    update_task_list()


# Task editing
def open_edit_dialog(task: dict) -> None:
    """Open a dialog to edit a task"""
    with ui.dialog() as dialog, ui.card():
        ui.label('Edit task').classes('text-xl font-bold mb-2')

        text_input = ui.input('Text', value=task['text']).classes('w-64')

        priority_input = ui.select(
            {
                'low': 'Low',
                'normal': 'Normal',
                'high': 'High',
            },
            value=task['priority'],
            label='Priority'
        ).classes('w-40')

        notes_input = ui.input(
            'Notes',
            value=task['notes'] or ''
        ).classes('w-64')

        with ui.row().classes('mt-4 gap-4'):
            ui.button(
                'Save',
                on_click=lambda: save_task_edit(
                    task,
                    text_input.value,
                    priority_input.value,
                    notes_input.value,
                    dialog
                )
            ).classes('bg-blue-600 text-white px-4 py-2 rounded')

            ui.button(
                'Cancel',
                on_click=dialog.close
            ).classes('bg-gray-400 text-white px-4 py-2 rounded')

    dialog.open()

def save_task_edit(
    task: dict,
    new_text: str,
    new_priority: str,
    new_notes: str,
    dialog
) -> None:
    """Save edited task values."""
    task['text'] = new_text.strip()
    task['priority'] = new_priority
    task['notes'] = new_notes.strip() if new_notes else None

    dialog.close()
    update_task_list()

# Theme handling
def toggle_dark_mode(enabled: bool) -> None:
    """Enable or disable dark mode"""
    ui.dark_mode().enable() if enabled else ui.dark_mode().disable()

# Exit APP
def exit_app() -> None:
    """Shut down the NiceGUI application."""
    ui.notify('Closing application...')
    app.shutdown()

# UI layout
with ui.row().classes('items-center justify-between w-full'):
    title = ui.label('Task List (0 pending)').classes('text-2xl font-bold')

    ui.switch(
        'Dark mode',
        on_change=lambda e: toggle_dark_mode(e.value)
    ).classes('text-lg ml-auto')

    ui.button(
        'Exit',
        on_click=exit_app
    ).classes('bg-red-600 text-white px-4 py-2 rounded')

with ui.row().classes('gap-4 mt-4'):
    task_input = ui.input('New task').classes('w-64')

    priority_selector = ui.select(
        {
            'low': 'Low',
            'normal': 'Normal',
            'high': 'High',
        },
        value='low',
        label='Priority'
    ).classes('w-40')

    notes_input = ui.input('Notes (optional)').classes('w-64')

    ui.button(
        'Add',
        on_click=add_task
    ).classes('bg-blue-600 text-white px-4 py-2 rounded')

tasks_container = ui.column().classes('mt-6 gap-2')

# Run UI
ui.run(title='Advanced Task List')
