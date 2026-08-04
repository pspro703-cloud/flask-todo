document.addEventListener('DOMContentLoaded', function() {
    // Auto-dismiss flash messages
    document.querySelectorAll('.flash-message').forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transition = 'opacity 0.5s';
            setTimeout(() => msg.remove(), 500);
        }, 4000);
    });

    // Toggle todo via AJAX
    document.querySelectorAll('.todo-toggle').forEach(checkbox => {
        checkbox.addEventListener('change', async function() {
            const todoId = this.dataset.id;
            const card = document.getElementById(`todo-${todoId}`);
            const title = document.getElementById(`title-${todoId}`);

            try {
                const response = await fetch(`/todo/${todoId}/toggle`, {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        'Content-Type': 'application/json'
                    }
                });
                const data = await response.json();

                if (data.status === 'completed') {
                    card.classList.add('bg-green-50', 'border-green-200');
                    title.classList.add('completed-strike');
                } else {
                    card.classList.remove('bg-green-50', 'border-green-200');
                    title.classList.remove('completed-strike');
                }

                // Update stats
                document.getElementById('stat-total').textContent = data.stats.total;
                document.getElementById('stat-pending').textContent = data.stats.pending;
                document.getElementById('stat-completed').textContent = data.stats.completed;

                // Update progress bar
                const percent = data.stats.total > 0
                    ? Math.round((data.stats.completed / data.stats.total) * 100)
                    : 0;
                document.getElementById('progress-bar').style.width = percent + '%';
                document.getElementById('progress-text').textContent = percent + '%';

            } catch (err) {
                console.error('Error:', err);
                this.checked = !this.checked;
            }
        });
    });

    // Confirm delete
    document.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            if (!confirm('Delete this todo?')) {
                e.preventDefault();
            }
        });
    });

    // Mobile menu
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
    }
});