from backend.celery import app

result = app.send_task('pwa.tasks.add', args=(4, 6))
print('Task ID:', result.id)
print('Waiting for result...')
print('Result:', result.get(timeout=10))
