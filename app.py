<!DOCTYPE html>
<html lang="ro">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Catalog Școlar - Panou Administrator</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.5/font/bootstrap-icons.css">
    <style>
        body {
            background-color: #f3f4f6;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar exact ca în imaginea ta (gri închis / negru) */
        .sidebar {
            width: 260px;
            background-color: #1f2229;
            color: #d1d5db;
            display: flex;
            flex-direction: column;
            flex-shrink: 0;
        }

        .user-profile {
            padding: 20px 15px;
            display: flex;
            align-items: center;
            gap: 12px;
            border-bottom: 1px solid #2d3139;
        }

        .user-avatar {
            width: 45px;
            height: 45px;
            background-color: #374151;
            color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 1.5rem;
            font-weight: bold;
        }

        .user-info .role {
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 2px;
            font-size: 0.9rem;
        }

        .user-info .year {
            color: #9ca3af;
            font-size: 0.8rem;
        }

        .nav-menu {
            list-style: none;
            padding: 0;
            margin: 10px 0;
            flex-grow: 1;
        }

        .nav-menu li a {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px 20px;
            color: #d1d5db;
            text-decoration: none;
            font-size: 0.9rem;
            font-weight: 500;
            border-bottom: 1px solid #2d3139;
            transition: all 0.2s;
        }

        .nav-menu li.active a, .nav-menu li a:hover {
            background-color: #ffffff;
            color: #111827;
            font-weight: 600;
        }

        .app-btn-container {
            padding: 15px;
        }

        .btn-add-app {
            background-color: #dc2626;
            color: white;
            border: none;
            width: 100%;
            padding: 10px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.9rem;
            text-align: center;
            display: block;
            text-decoration: none;
        }

        .btn-add-app:hover {
            background-color: #b91c1c;
            color: white;
        }

        /* Zona Principală */
        .main-content {
            flex-grow: 1;
            padding: 0;
            overflow-y: auto;
        }

        .top-header {
            background-color: #e5e7eb;
            padding: 12px 25px;
            font-weight: 700;
            font-size: 1.1rem;
            color: #111827;
            border-bottom: 1px solid #d1d5db;
        }

        .content-container {
            padding: 25px 30px;
            max-width: 1200px;
            margin: 0 auto;
        }

        .card-custom {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
            margin-bottom: 20px;
        }

        .section-title {
            font-weight: 700;
            font-size: 1rem;
            color: #111827;
            margin-bottom: 15px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
    </style>
</head>
<body>

    <!-- Sidebar exact după cerință -->
    <div class="sidebar">
        <div class="user-profile">
            <div class="user-avatar">A</div>
            <div class="user-info">
                <div class="role">Administrator</div>
                <div class="year">An școlar: 2026/2027</div>
            </div>
        </div>

        <ul class="nav-menu">
            <li class="active"><a href="/dashboard">Acasă <i class="bi bi-house-door-fill"></i></a></li>
            <li><a href="#">Orar <i class="bi bi-clock"></i></a></li>
            <li><a href="#">Calendar școlar <i class="bi bi-calendar-event"></i></a></li>
            <li><a href="#">Bibliotecă <i class="bi bi-book"></i></a></li>
            <li><a href="#">Manuale digitale <i class="bi bi-journal-bookmark"></i></a></li>
            <li><a href="#">Reviste școlare <i class="bi bi-journal-text"></i></a></li>
            <li><a href="#">Documente și formulare <i class="bi bi-file-earmark-text"></i></a></li>
            <li><a href="#">Setări <i class="bi bi-gear"></i></a></li>
            <li><a href="#">Ajutor <i class="bi bi-info-circle"></i></a></li>
            <li><a href="/logout">Ieșire <i class="bi bi-power"></i></a></li>
        </ul>

        <div class="app-btn-container">
            <a href="#" class="btn-add-app">Adaugă ca aplicație</a>
        </div>
    </div>

    <!-- Conținut Principal (Fără butonul roșu de deconectare de sus) -->
    <div class="main-content">
        <div class="top-header">Acasă</div>

        <div class="content-container">
            
            {% with messages = get_flashed_messages(with_categories=true) %}
              {% if messages %}
                {% for category, message in messages %}
                  <div class="alert alert-{{ category }} alert-dismissible fade show shadow-sm" role="alert">
                    {{ message }}
                    <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
                  </div>
                {% endfor %}
              {% endif %}
            {% endwith %}

            <!-- Formulare Administrare: Adaugă Elev, Notă, Absență -->
            <div class="row">
                <div class="col-md-4 mb-4">
                    <div class="card-custom h-100">
                        <div class="section-title text-dark"><i class="bi bi-person-plus-fill"></i> Adaugă Elev Nou</div>
                        <form action="/admin/creeaza_elev" method="POST">
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Nume și Prenume</label>
                                <input type="text" class="form-control" name="nume" required placeholder="ex: Popescu Ion">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Clasa</label>
                                <input type="text" class="form-control" name="clasa" required placeholder="ex: 10A">
                            </div>
                            <button type="submit" class="btn btn-dark w-100 fw-bold">Salvează Elev</button>
                        </form>
                    </div>
                </div>

                <div class="col-md-4 mb-4">
                    <div class="card-custom h-100">
                        <div class="section-title text-dark"><i class="bi bi-journal-plus"></i> Adaugă Notă</div>
                        <form action="/admin/adauga_nota" method="POST">
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Elev</label>
                                <select class="form-select" name="elev_id" required>
                                    <option value="">-- Selectează elev --</option>
                                    {% for e in elevi %}
                                        <option value="{{ e.id }}">{{ e.nume }} ({{ e.clasa }})</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Materie</label>
                                <input type="text" class="form-control" name="materie" required placeholder="ex: Matematică">
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Notă (1-10)</label>
                                <input type="number" class="form-control" name="valoare" min="1" max="10" required>
                            </div>
                            <button type="submit" class="btn btn-secondary w-100 fw-bold">Adaugă Notă</button>
                        </form>
                    </div>
                </div>

                <div class="col-md-4 mb-4">
                    <div class="card-custom h-100">
                        <div class="section-title text-dark"><i class="bi bi-exclamation-triangle-fill"></i> Adaugă Absență</div>
                        <form action="/admin/adauga_absenta" method="POST">
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Elev</label>
                                <select class="form-select" name="elev_id" required>
                                    <option value="">-- Selectează elev --</option>
                                    {% for e in elevi %}
                                        <option value="{{ e.id }}">{{ e.nume }} ({{ e.clasa }})</option>
                                    {% endfor %}
                                </select>
                            </div>
                            <div class="mb-3">
                                <label class="form-label small fw-bold">Materie</label>
                                <input type="text" class="form-control" name="materie" required placeholder="ex: Fizică">
                            </div>
                            <button type="submit" class="btn btn-dark w-100 fw-bold mt-4">Adaugă Absență</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- Cereri Înregistrare Utilizatori -->
            <div class="card-custom">
                <div class="section-title text-dark"><i class="bi bi-people-fill"></i> Cereri de Înregistrare Utilizatori (În Așteptare)</div>
                {% if cereri %}
                    <div class="table-responsive">
                        <table class="table table-hover align-middle">
                            <thead class="table-light">
                                <tr>
                                    <th>Nume</th>
                                    <th>Email</th>
                                    <th>Rol Solicitat</th>
                                    <th>Atribuie Elev</th>
                                    <th>Acțiuni</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for c in cereri %}
                                <tr>
                                    <td class="fw-bold">{{ c.nume }}</td>
                                    <td>{{ c.email }}</td>
                                    <td><span class="badge bg-secondary">{{ c.rol }}</span></td>
                                    <td>
                                        <form action="/admin/aprobe_user/{{ c.id }}" method="POST" class="d-flex gap-2">
                                            <select name="elev_id" class="form-select form-select-sm">
                                                <option value="">-- Niciun elev --</option>
                                                {% for e in elevi %}
                                                    <option value="{{ e.id }}">{{ e.nume }} ({{ e.clasa }})</option>
                                                {% endfor %}
                                            </select>
                                            <input type="hidden" name="rol" value="{{ c.rol }}">
                                            <button type="submit" class="btn btn-sm btn-dark fw-bold">Aprobă</button>
                                        </form>
                                    </td>
                                    <td>
                                        <a href="/admin/respinge_user/{{ c.id }}" class="btn btn-sm btn-outline-secondary">Respinge</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p class="text-muted mb-0 small">Nu există cereri noi în așteptare momentan.</p>
                {% endif %}
            </div>

            <!-- Situația Elevilor -->
            <div class="card-custom">
                <div class="section-title text-dark"><i class="bi bi-table"></i> Situația Elevilor din Catalog</div>
                {% if elevi %}
                    <div class="table-responsive">
                        <table class="table table-striped align-middle">
                            <thead class="table-dark">
                                <tr>
                                    <th>Nume Elev</th>
                                    <th>Clasă</th>
                                    <th>Media Generală</th>
                                    <th>Note</th>
                                    <th>Absențe</th>
                                    <th>Acțiuni</th>
                                </tr>
                            </thead>
                            <tbody>
                                {% for e in elevi %}
                                <tr>
                                    <td class="fw-bold text-uppercase">{{ e.nume }}</td>
                                    <td><span class="badge bg-secondary">{{ e.clasa }}</span></td>
                                    <td>
                                        {% set medie = e.calculeaza_medie() %}
                                        {% if medie > 0 %}
                                            <span class="badge bg-dark fs-6">{{ medie }}</span>
                                        {% else %}
                                            <span class="text-muted small">-</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if e.note %}
                                            {% for n in e.note %}
                                                <span class="badge bg-secondary me-1">{{ n.materie }}: {{ n.valoare }}</span>
                                            {% endfor %}
                                        {% else %}
                                            <span class="text-muted small">Fără note</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        {% if e.absente %}
                                            {% for a in e.absente %}
                                                <span class="badge bg-dark me-1">{{ a.materie }}</span>
                                            {% endfor %}
                                        {% else %}
                                            <span class="text-muted small">Fără absențe</span>
                                        {% endif %}
                                    </td>
                                    <td>
                                        <a href="/admin/sterge_elev/{{ e.id }}" class="btn btn-sm btn-outline-danger" onclick="return confirm('Sigur ștergi acest elev?')"><i class="bi bi-trash"></i> Șterge</a>
                                    </td>
                                </tr>
                                {% endfor %}
                            </tbody>
                        </table>
                    </div>
                {% else %}
                    <p class="text-muted mb-0 small">Nu există elevi adăugați în catalog încă.</p>
                {% endif %}
            </div>

        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>