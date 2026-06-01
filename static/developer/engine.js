document.addEventListener('DOMContentLoaded', function() {
    if (sessionStorage.getItem('devModeRecording') === '1') {
        buildRecordingUI();
        return;
    }

    if (sessionStorage.getItem('devModePresenting') === '1') {
        buildPlaybackUI();
        return;
    }

    var brand = document.getElementById('navbar-brand-link');
    if (!brand) return;
    var isAdminUser = brand.dataset.adminUser === '1';

    function getCsrfToken() {
        var match = document.cookie.match(/csrftoken=([^;]+)/);
        return match ? match[1] : '';
    }

    function getElementDesc(el) {
        if (!el) return '';
        var desc = el.tagName.toLowerCase();
        if (el.id) desc += '#' + el.id;
        if (el.className && typeof el.className === 'string') {
            var cls = el.className.trim().split(/\s+/).slice(0, 3).join('.');
            if (cls) desc += '.' + cls;
        }
        var text = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 50);
        if (text) desc += ' "' + text + '"';
        return desc;
    }

    function getElementInfo(el) {
        if (!el) return {};
        var info = {};
        var tag = el.tagName.toLowerCase();
        info.tagName = tag;
        var sel = tag;
        if (el.id) { sel += '#' + el.id; }
        if (el.className && typeof el.className === 'string') {
            var cls = el.className.trim().split(/\s+/).slice(0, 3).join('.');
            if (cls) sel += '.' + cls;
        }
        info.sel = sel;
        var rawText = (el.innerText || el.textContent || '').trim().replace(/\s+/g, ' ').slice(0, 80);
        if (rawText) info.text = rawText;
        var href = el.getAttribute('href');
        if (href) info.href = href;
        var name = el.getAttribute('name');
        if (name) info.name = name;
        var ariaLabel = el.getAttribute('aria-label');
        if (ariaLabel) info.ariaLabel = ariaLabel;
        if (el.title) info.title = el.title;
        var placeholder = el.getAttribute('placeholder');
        if (placeholder) info.placeholder = placeholder;
        if (tag === 'input') info.inputType = (el.type || 'text').toLowerCase();
        var anchor = el.closest && el.closest('a');
        if (anchor && anchor !== el) {
            var parentHref = anchor.getAttribute('href');
            if (parentHref) info.parentHref = parentHref;
        }
        return info;
    }

    function isTextInput(el) {
        if (!el) return false;
        var tag = el.tagName.toLowerCase();
        if (tag === 'textarea') return true;
        if (tag === 'input') {
            var t = (el.type || 'text').toLowerCase();
            return ['text', 'search', 'email', 'password', 'number', 'tel', 'url', ''].indexOf(t) !== -1;
        }
        return false;
    }

    function buildRecordingUI() {
        var toolbar = document.createElement('div');
        toolbar.id = 'dev-toolbar';
        toolbar.style.cssText = 'position:fixed;top:10px;left:10px;z-index:99999;display:flex;flex-direction:column;gap:6px;';

        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:6px;';

        var recLabel = document.createElement('button');
        recLabel.textContent = '● REC';
        recLabel.disabled = true;
        recLabel.style.cssText = 'background:red;color:white;border:none;padding:3px 10px;cursor:default;width:70px;';

        var stopBtn = document.createElement('button');
        stopBtn.textContent = '■ Stop';
        stopBtn.style.cssText = 'background:green;color:white;border:none;padding:3px 10px;cursor:pointer;width:70px;';

        btnRow.appendChild(recLabel);
        btnRow.appendChild(stopBtn);
        toolbar.appendChild(btnRow);

        var jsonBox = document.createElement('textarea');
        jsonBox.style.cssText = 'display:block;width:320px;height:200px;font-family:monospace;font-size:12px;resize:both;';
        jsonBox.readOnly = true;
        toolbar.appendChild(jsonBox);
        document.body.appendChild(toolbar);

        var coords = document.createElement('div');
        coords.id = 'dev-mouse-coords';
        coords.style.cssText = 'position:fixed;z-index:99999;pointer-events:none;font-size:11px;font-family:monospace;background:rgba(0,0,0,0.75);color:#fff;padding:2px 6px;border-radius:3px;display:none;';
        document.body.appendChild(coords);

        document.addEventListener('mousemove', function(e) {
            coords.style.display = 'block';
            coords.style.left = (e.clientX + 14) + 'px';
            coords.style.top = (e.clientY + 14) + 'px';
            coords.textContent = e.clientX + ', ' + e.clientY;
        });

        setupRecording(toolbar, recLabel, stopBtn, jsonBox);
    }

    function applyDevModeVisuals(showNotification) {
        var nameEl = document.getElementById('lf-greeting-name');
        if (nameEl) {
            nameEl.textContent = 'Developer';
            nameEl.style.color = 'var(--success-color)';
        }

        var toolbar = document.createElement('div');
        toolbar.id = 'dev-toolbar';
        toolbar.style.cssText = 'position:fixed;top:10px;left:10px;z-index:99999;display:flex;flex-direction:column;gap:6px;';

        var btnRow = document.createElement('div');
        btnRow.style.cssText = 'display:flex;gap:6px;';

        var recordBtn = document.createElement('button');
        recordBtn.textContent = 'Record';
        recordBtn.style.cssText = 'background:red;color:white;border:none;padding:3px 10px;cursor:pointer;width:70px;';

        var presentBtn = document.createElement('button');
        presentBtn.textContent = 'Present';
        presentBtn.style.cssText = 'background:green;color:white;border:none;padding:3px 10px;cursor:pointer;width:70px;';

        btnRow.appendChild(recordBtn);
        btnRow.appendChild(presentBtn);
        toolbar.appendChild(btnRow);

        var jsonBox = document.createElement('textarea');
        jsonBox.style.cssText = 'display:none;width:320px;height:200px;font-family:monospace;font-size:12px;resize:both;';
        toolbar.appendChild(jsonBox);
        document.body.appendChild(toolbar);

        var coords = document.createElement('div');
        coords.id = 'dev-mouse-coords';
        coords.style.cssText = 'position:fixed;z-index:99999;pointer-events:none;font-size:11px;font-family:monospace;background:rgba(0,0,0,0.75);color:#fff;padding:2px 6px;border-radius:3px;display:none;';
        document.body.appendChild(coords);

        document.addEventListener('mousemove', function(e) {
            coords.style.display = 'block';
            coords.style.left = (e.clientX + 14) + 'px';
            coords.style.top = (e.clientY + 14) + 'px';
            coords.textContent = e.clientX + ', ' + e.clientY;
        });

        var pendingSnapshot = null;

        presentBtn.addEventListener('click', function() {
            if (presentBtn.textContent === 'Present') {
                presentBtn.textContent = '...';
                presentBtn.disabled = true;
                fetch('/developer/api/instructions/', { credentials: 'same-origin' })
                    .then(function(r) { if (!r.ok) throw new Error(); return r.json(); })
                    .then(function(data) {
                        pendingSnapshot = data;
                        jsonBox.value = JSON.stringify(data, null, 2);
                        jsonBox.style.display = 'block';
                        presentBtn.textContent = 'Confirm';
                        presentBtn.disabled = false;
                        recordBtn.textContent = 'Reject';
                    })
                    .catch(function() {
                        presentBtn.textContent = 'Present';
                        presentBtn.disabled = false;
                    });
            } else if (presentBtn.textContent === 'Confirm') {
                if (!pendingSnapshot) return;
                var snapshotStr = JSON.stringify(pendingSnapshot);
                presentBtn.disabled = true;
                presentBtn.textContent = '...';
                fetch('/developer/api/load-snapshot/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    body: snapshotStr
                }).then(function(r) {
                    if (!r.ok) throw new Error('failed');
                    return r.json();
                }).then(function() {
                    sessionStorage.setItem('devModePlaybackInstructions', JSON.stringify(pendingSnapshot.instructions || []));
                    sessionStorage.setItem('devModePlaybackIndex', '0');
                    sessionStorage.setItem('devModePresenting', '1');
                    return fetch('/developer/api/begin-recording/', {
                        method: 'POST',
                        credentials: 'same-origin',
                        headers: { 'X-CSRFToken': getCsrfToken() }
                    });
                }).then(function(r) {
                    if (!r.ok) throw new Error('logout failed');
                    return r.json();
                }).then(function(d) {
                    sessionStorage.setItem('devModeReloginToken', d.token);
                    window.location.href = '/';
                }).catch(function() {
                    presentBtn.disabled = false;
                    presentBtn.textContent = 'Confirm';
                });
            }
        });

        recordBtn.addEventListener('click', function() {
            if (recordBtn.textContent === 'Reject') {
                jsonBox.style.display = 'none';
                presentBtn.textContent = 'Present';
                recordBtn.textContent = 'Record';
            } else if (recordBtn.textContent === 'Record') {
                performRecord(toolbar, recordBtn, presentBtn, jsonBox);
            }
        });

        var savedNotify = sessionStorage.getItem('devModeSaved') === '1';
        if (savedNotify) sessionStorage.removeItem('devModeSaved');

        if (!showNotification && !savedNotify) return;

        var container = document.querySelector('.flash-messages-container');
        if (!container) {
            container = document.createElement('div');
            container.className = 'flash-messages-container';
            document.body.insertBefore(container, document.body.firstChild);
        }

        var alertEl = document.createElement('div');
        alertEl.className = 'alert alert-success flash-message';

        var icon = document.createElement('i');
        icon.className = 'fas fa-check-circle';

        var text = document.createElement('span');
        text.textContent = savedNotify ? 'Saved.' : 'You have entered Developer Mode.';

        var closeBtn = document.createElement('button');
        closeBtn.className = 'alert-close';
        closeBtn.innerHTML = '&times;';
        closeBtn.onclick = function() { alertEl.remove(); };

        alertEl.appendChild(icon);
        alertEl.appendChild(text);
        alertEl.appendChild(closeBtn);
        container.appendChild(alertEl);

        setTimeout(function() {
            alertEl.setAttribute('aria-live', 'off');
            alertEl.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
            alertEl.style.opacity = '0';
            alertEl.style.transform = 'translateY(-6px)';
            setTimeout(function() { alertEl.remove(); }, 300);
        }, 4500);
    }

    function performRecord(toolbar, recordBtn, presentBtn, jsonBox) {
        recordBtn.disabled = true;
        recordBtn.textContent = '...';

        fetch('/developer/api/snapshot/', { credentials: 'same-origin' })
            .then(function(r) {
                if (!r.ok) throw new Error('Snapshot failed');
                return r.json();
            })
            .then(function(data) {
                return fetch('/developer/api/save/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCsrfToken()
                    },
                    body: JSON.stringify(data)
                }).then(function(r) {
                    if (!r.ok) throw new Error('Save failed');
                    return data;
                });
            })
            .then(function(data) {
                recordBtn.textContent = 'Delete';
                recordBtn.disabled = false;
                presentBtn.textContent = 'Keep';

                function cleanup() {
                    recordBtn.removeEventListener('click', onDelete);
                    presentBtn.removeEventListener('click', onKeep);
                }

                function onDelete() {
                    cleanup();
                    data.instructions = [];
                    sessionStorage.setItem('devModeSnapshot', JSON.stringify(data));
                    sessionStorage.setItem('devModeInstructions', '[]');
                    sessionStorage.setItem('devModeRecording', '1');
                    fetch('/developer/api/begin-recording/', {
                        method: 'POST',
                        credentials: 'same-origin',
                        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                        body: '{}'
                    }).then(function(r) { return r.json(); })
                    .then(function(resp) {
                        sessionStorage.setItem('devModeReloginToken', resp.token);
                        window.location.href = '/';
                    }).catch(function() {
                        window.location.href = '/';
                    });
                }

                function onKeep() {
                    cleanup();
                    recordBtn.textContent = 'Record';
                    presentBtn.textContent = 'Present';
                }

                recordBtn.addEventListener('click', onDelete);
                presentBtn.addEventListener('click', onKeep);
            })
            .catch(function() {
                recordBtn.textContent = 'Error';
                recordBtn.disabled = true;
                setTimeout(function() {
                    recordBtn.textContent = 'Record';
                    recordBtn.disabled = false;
                }, 1500);
            });
    }

    function setupRecording(toolbar, recordBtn, presentBtn, jsonBox) {
        var instructions = JSON.parse(sessionStorage.getItem('devModeInstructions') || '[]');
        var recordingActive = true;

        recordBtn.textContent = 'REC';
        recordBtn.disabled = true;
        presentBtn.textContent = 'Stop';

        jsonBox.style.display = 'block';
        jsonBox.readOnly = true;
        refreshJsonBox();

        function refreshJsonBox() {
            jsonBox.value = instructions.length > 0
                ? JSON.stringify(instructions[instructions.length - 1], null, 2)
                : '';
        }

        function commitInstruction(instr) {
            instructions.push(instr);
            sessionStorage.setItem('devModeInstructions', JSON.stringify(instructions));
            refreshJsonBox();
        }

        var state = 'idle';
        var currentTyping = '';
        var pendingDown = null;
        var mouseButtonHeld = false;

        function commitTyping() {
            if (currentTyping) {
                commitInstruction({ type: 'type', text: currentTyping });
                currentTyping = '';
            }
            if (state === 'typing') state = 'textbox_wait';
        }

        document.addEventListener('mousedown', function(e) {
            if (!recordingActive || toolbar.contains(e.target)) return;
            mouseButtonHeld = true;
            commitTyping();
            pendingDown = {
                pos: { x: e.clientX, y: e.clientY },
                info: getElementInfo(e.target),
                isText: isTextInput(e.target)
            };
        }, true);

        document.addEventListener('mouseup', function(e) {
            mouseButtonHeld = false;
            if (!recordingActive || toolbar.contains(e.target)) return;
            if (!pendingDown) return;
            var info = pendingDown.info;
            var instr = { type: 'click', start: pendingDown.pos, end: { x: e.clientX, y: e.clientY }, target: info.sel };
            if (info.tagName) instr.tagName = info.tagName;
            if (info.text) instr.text = info.text;
            if (info.href) instr.href = info.href;
            if (info.parentHref) instr.parentHref = info.parentHref;
            if (info.name) instr.name = info.name;
            if (info.ariaLabel) instr.ariaLabel = info.ariaLabel;
            if (info.title) instr.title = info.title;
            if (info.placeholder) instr.placeholder = info.placeholder;
            if (info.inputType) instr.inputType = info.inputType;
            commitInstruction(instr);
            state = pendingDown.isText ? 'textbox_wait' : 'idle';
            pendingDown = null;
        }, true);

        var mouseX = 0;
        var mouseY = 0;

        document.addEventListener('mousemove', function(e) {
            mouseX = e.clientX;
            mouseY = e.clientY;
            if (!recordingActive || mouseButtonHeld) return;
            if (state === 'typing') commitTyping();
        });

        var scrollTimer = null;
        var lastScrollY = window.scrollY;
        var lastScrollX = window.scrollX;

        window.addEventListener('scroll', function() {
            if (!recordingActive) return;
            if (scrollTimer === null) {
                commitInstruction({ type: 'move', position: { x: mouseX, y: mouseY } });
            }
            clearTimeout(scrollTimer);
            scrollTimer = setTimeout(function() {
                var x = window.scrollX;
                var y = window.scrollY;
                commitInstruction({
                    type: 'scroll',
                    amount: Math.round(y - lastScrollY),
                    position: { x: Math.round(x), y: Math.round(y) }
                });
                lastScrollX = x;
                lastScrollY = y;
                scrollTimer = null;
            }, 250);
        }, { passive: true });

        document.addEventListener('keydown', function(e) {
            if (!recordingActive) return;

            if (e.key === 'Escape') {
                e.preventDefault();
                stopRecording();
                return;
            }

            if (state === 'idle') return;

            if (e.key === 'Enter') {
                currentTyping += '\n';
                commitInstruction({ type: 'type', text: currentTyping });
                currentTyping = '';
                state = 'textbox_wait';
                return;
            }

            if (e.key === 'Tab') {
                commitTyping();
                commitInstruction({ type: 'tab' });
                state = 'textbox_wait';
                return;
            }

            if (e.key === 'Backspace') {
                if (currentTyping.length > 0) currentTyping = currentTyping.slice(0, -1);
                state = 'typing';
                return;
            }

            if (e.key.length === 1) {
                currentTyping += e.key;
                state = 'typing';
            }
        }, true);

        presentBtn.addEventListener('click', function() {
            stopRecording();
        });

        function stopRecording() {
            recordingActive = false;
            commitTyping();
            var snapshot = JSON.parse(sessionStorage.getItem('devModeSnapshot') || '{}');
            snapshot.instructions = instructions;
            var token = sessionStorage.getItem('devModeReloginToken');
            function doSave() {
                fetch('/developer/api/save/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    body: JSON.stringify(snapshot)
                }).then(function() {
                    sessionStorage.removeItem('devModeRecording');
                    sessionStorage.removeItem('devModeInstructions');
                    sessionStorage.removeItem('devModeSnapshot');
                    sessionStorage.removeItem('devModeReloginToken');
                    sessionStorage.setItem('devModeSaved', '1');
                    window.location.href = '/';
                }).catch(function() {
                    window.location.href = '/';
                });
            }
            if (token) {
                fetch('/developer/api/relogin/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    body: JSON.stringify({ token: token })
                }).then(function() { doSave(); }).catch(function() { doSave(); });
            } else {
                doSave();
            }
        }
    }

    function buildPlaybackUI() {
        var instructions = JSON.parse(sessionStorage.getItem('devModePlaybackInstructions') || '[]');
        var index = parseInt(sessionStorage.getItem('devModePlaybackIndex') || '0', 10);
        var speedUp = false;
        var actionPlaying = false;
        var lastTextEl = null;

        var SVG_ARROW = '<svg viewBox="0 0 24 26" width="18" height="20" xmlns="http://www.w3.org/2000/svg"><path d="M4 0 L4 20 L8 15 L12 23 L15 22 L11 14 L18 14 Z" fill="white" stroke="#111" stroke-width="1.5" stroke-linejoin="round" stroke-linecap="round"/></svg>';
        var SVG_IBEAM = '<svg viewBox="0 0 16 24" width="13" height="22" xmlns="http://www.w3.org/2000/svg"><line x1="8" y1="3" x2="8" y2="21" stroke="white" stroke-width="4" stroke-linecap="round"/><line x1="8" y1="3" x2="8" y2="21" stroke="#111" stroke-width="1.5" stroke-linecap="round"/><line x1="4" y1="3" x2="12" y2="3" stroke="white" stroke-width="4"/><line x1="4" y1="3" x2="12" y2="3" stroke="#111" stroke-width="1.5"/><line x1="4" y1="21" x2="12" y2="21" stroke="white" stroke-width="4"/><line x1="4" y1="21" x2="12" y2="21" stroke="#111" stroke-width="1.5"/></svg>';

        var cursor = document.createElement('div');
        cursor.style.cssText = 'position:fixed;z-index:2147483647;pointer-events:none;filter:drop-shadow(1px 1px 1px rgba(0,0,0,0.35));';
        cursor.innerHTML = SVG_ARROW;
        document.body.appendChild(cursor);

        var cursorX = parseFloat(sessionStorage.getItem('devModeCursorX')) || window.innerWidth / 2;
        var cursorY = parseFloat(sessionStorage.getItem('devModeCursorY')) || window.innerHeight / 2;
        cursor.style.left = cursorX + 'px';
        cursor.style.top = cursorY + 'px';

        var overlay = document.createElement('div');
        overlay.style.cssText = 'position:fixed;z-index:2147483646;top:0;left:0;width:100%;height:100%;cursor:default;';
        document.body.appendChild(overlay);

        function updateCursorStyle(x, y) {
            overlay.style.pointerEvents = 'none';
            var elUnder = document.elementFromPoint(x, y);
            overlay.style.pointerEvents = '';
            if (elUnder && isTextInput(elUnder)) {
                cursor.innerHTML = SVG_IBEAM;
                cursor.style.transform = 'translateX(-6px)';
            } else {
                cursor.innerHTML = SVG_ARROW;
                cursor.style.transform = '';
            }
        }

        var hud = document.createElement('div');
        hud.style.cssText = 'position:fixed;bottom:12px;right:12px;z-index:2147483648;background:transparent;color:rgba(0,0,0,0.22);font-family:monospace;font-size:11px;padding:0;border-radius:0;pointer-events:none;letter-spacing:0.4px;';
        document.body.appendChild(hud);

        function updateHUD() {
            var pct = instructions.length ? Math.round(Math.min(index, instructions.length) / instructions.length * 100) : 0;
            hud.textContent = index + ' / ' + instructions.length + '  ' + pct + '%';
        }
        updateHUD();

        overlay.addEventListener('click', function() {
            if (actionPlaying) {
                speedUp = true;
            } else if (index < instructions.length) {
                executeNext();
            }
            // at end: clicks do nothing
        });

        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') { e.preventDefault(); exitPresentation(); return; }
            e.preventDefault();
            e.stopImmediatePropagation();
        }, true);
        document.addEventListener('keypress', function(e) { e.preventDefault(); e.stopImmediatePropagation(); }, true);
        window.addEventListener('wheel', function(e) { e.preventDefault(); }, { capture: true, passive: false });
        window.addEventListener('touchmove', function(e) { e.preventDefault(); }, { capture: true, passive: false });
        document.body.style.overflow = 'hidden';

        function executeNext() {
            var instr = instructions[index];
            index++;
            sessionStorage.setItem('devModePlaybackIndex', String(index));
            actionPlaying = true;
            speedUp = false;
            updateHUD();
            executeAction(instr, function() {
                actionPlaying = false;
                speedUp = false;
                updateHUD();
            });
        }

        function exitPresentation() {
            sessionStorage.removeItem('devModePresenting');
            sessionStorage.removeItem('devModePlaybackInstructions');
            sessionStorage.removeItem('devModePlaybackIndex');
            sessionStorage.removeItem('devModeCursorX');
            sessionStorage.removeItem('devModeCursorY');
            document.body.style.overflow = '';
            var token = sessionStorage.getItem('devModeReloginToken');
            if (token) {
                sessionStorage.removeItem('devModeReloginToken');
                fetch('/developer/api/relogin/', {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
                    body: JSON.stringify({ token: token })
                }).then(function() {
                    window.location.href = '/';
                }).catch(function() {
                    window.location.href = '/';
                });
            } else {
                window.location.href = '/';
            }
        }

        function moveCursor(tx, ty, onDone) {
            var sx = cursorX, sy = cursorY;
            var startTs = null;
            function frame(ts) {
                if (!startTs) startTs = ts;
                var dur = speedUp ? 60 : 600;
                var t = Math.min((ts - startTs) / dur, 1);
                var ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
                cursorX = sx + (tx - sx) * ease;
                cursorY = sy + (ty - sy) * ease;
                cursor.style.left = cursorX + 'px';
                cursor.style.top = cursorY + 'px';
                if (t < 1) { requestAnimationFrame(frame); }
                else { cursorX = tx; cursorY = ty; sessionStorage.setItem('devModeCursorX', String(tx)); sessionStorage.setItem('devModeCursorY', String(ty)); cursor.style.left = tx + 'px'; cursor.style.top = ty + 'px'; updateCursorStyle(tx, ty); onDone(); }
            }
            requestAnimationFrame(frame);
        }

        function showRipple(x, y, onDone) {
            var fast = speedUp;
            var d = fast ? '0.1s' : '0.3s';
            var r = document.createElement('div');
            r.style.cssText = 'position:fixed;z-index:2147483645;pointer-events:none;border-radius:50%;border:2px solid rgba(255,80,0,0.9);background:rgba(255,80,0,0.18);width:16px;height:16px;transform:translate(-50%,-50%);left:' + x + 'px;top:' + y + 'px;transition:width ' + d + ',height ' + d + ',opacity ' + d + ';';
            document.body.appendChild(r);
            setTimeout(function() { r.style.width = '56px'; r.style.height = '56px'; r.style.opacity = '0'; }, 10);
            setTimeout(function() { r.remove(); onDone(); }, fast ? 130 : 360);
        }

        function findEl(instr) {
            if (!instr) return null;
            var sel = typeof instr === 'string' ? instr : instr.target;
            // 1. Exact CSS selector
            if (sel) {
                try { var r = document.querySelector(sel); if (r) return r; } catch(ex) {}
            }
            // 2. ID only
            if (sel) {
                var idM = sel.match(/#([^.\[\s:]+)/);
                if (idM) { var byId = document.getElementById(idM[1]); if (byId) return byId; }
            }
            if (typeof instr === 'string') return null;
            // 3. href (anchor)
            if (instr.href) {
                try { var byHref = document.querySelector('a[href="' + instr.href.replace(/"/g, '\\"') + '"]'); if (byHref) return byHref; } catch(ex) {}
            }
            // 4. parentHref (element inside anchor)
            if (instr.parentHref) {
                try { var byPHref = document.querySelector('a[href="' + instr.parentHref.replace(/"/g, '\\"') + '"]'); if (byPHref) return byPHref; } catch(ex) {}
            }
            // 5. name attribute
            if (instr.name) {
                try { var byName = document.querySelector('[name="' + instr.name.replace(/"/g, '\\"') + '"]'); if (byName) return byName; } catch(ex) {}
            }
            // 6. aria-label
            if (instr.ariaLabel) {
                try { var byAria = document.querySelector('[aria-label="' + instr.ariaLabel.replace(/"/g, '\\"') + '"]'); if (byAria) return byAria; } catch(ex) {}
            }
            // 7. placeholder
            if (instr.placeholder) {
                try { var byPH = document.querySelector('[placeholder="' + instr.placeholder.replace(/"/g, '\\"') + '"]'); if (byPH) return byPH; } catch(ex) {}
            }
            // 8. text content + tagName
            if (instr.text && instr.tagName) {
                var nodes = document.querySelectorAll(instr.tagName);
                for (var ni = 0; ni < nodes.length; ni++) {
                    var nt = (nodes[ni].innerText || nodes[ni].textContent || '').trim().replace(/\s+/g, ' ');
                    if (nt === instr.text || nt.indexOf(instr.text) === 0) return nodes[ni];
                }
            }
            return null;
        }

        function getCenter(el) {
            var rect = el.getBoundingClientRect();
            return { x: Math.round(rect.left + rect.width / 2), y: Math.round(rect.top + rect.height / 2) };
        }

        function executeAction(instr, onDone) {
            if (instr.type === 'move') {
                moveCursor(instr.position.x, instr.position.y, onDone);
            } else if (instr.type === 'scroll') {
                doScroll(instr.position.x, instr.position.y, onDone);
            } else if (instr.type === 'click') {
                doClick(instr, onDone);
            } else if (instr.type === 'type') {
                doType(instr.text || '', onDone);
            } else if (instr.type === 'tab') {
                var active = document.activeElement;
                if (active) {
                    active.dispatchEvent(new KeyboardEvent('keydown', { key: 'Tab', code: 'Tab', keyCode: 9, bubbles: true, cancelable: true }));
                    active.dispatchEvent(new KeyboardEvent('keyup',   { key: 'Tab', code: 'Tab', keyCode: 9, bubbles: true }));
                }
                setTimeout(onDone, speedUp ? 40 : 120);
            } else {
                onDone();
            }
        }

        function doScroll(tx, ty, onDone) {
            var sx = window.scrollX, sy = window.scrollY;
            var startTs = null;
            function frame(ts) {
                if (!startTs) startTs = ts;
                var dur = speedUp ? 70 : 700;
                var t = Math.min((ts - startTs) / dur, 1);
                var ease = t < 0.5 ? 2*t*t : -1+(4-2*t)*t;
                window.scrollTo(sx + (tx - sx) * ease, sy + (ty - sy) * ease);
                if (t < 1) { requestAnimationFrame(frame); }
                else { window.scrollTo(tx, ty); onDone(); }
            }
            requestAnimationFrame(frame);
        }

        function doClick(instr, onDone) {
            var el = findEl(instr);
            var pos = el ? getCenter(el) : (instr.end || instr.start || { x: 0, y: 0 });
            moveCursor(pos.x, pos.y, function() {
                if (!el) { onDone(); return; }
                overlay.style.pointerEvents = 'none';
                var didNavigate = false;
                window.addEventListener('beforeunload', function() { didNavigate = true; }, { once: true });
                el.click();
                if (isTextInput(el)) lastTextEl = el;
                setTimeout(function() {
                    if (!didNavigate) { overlay.style.pointerEvents = ''; onDone(); }
                }, 200);
            });
        }

        function doType(text, onDone) {
            var el = document.activeElement;
            if (!el || !isTextInput(el)) el = lastTextEl;
            if (!el || !isTextInput(el)) {
                overlay.style.pointerEvents = 'none';
                el = document.elementFromPoint(cursorX, cursorY);
                overlay.style.pointerEvents = '';
            }
            if (!el || !isTextInput(el)) { onDone(); return; }
            lastTextEl = el;
            el.focus();
            var i = 0;
            function next() {
                if (i >= text.length) { onDone(); return; }
                var ch = text[i++];
                el.value += ch;
                el.dispatchEvent(new Event('input', { bubbles: true }));
                setTimeout(next, speedUp ? 40 : 92);
            }
            next();
        }
    }

    var logoutLink = document.getElementById('navbar-logout-link');
    if (logoutLink) {
        logoutLink.addEventListener('click', function() {
            ['devMode','devModeRecording','devModeSnapshot','devModeInstructions',
             'devModeSaved','devModeReloginToken','devModePresenting',
             'devModePlaybackInstructions','devModePlaybackIndex',
             'devModeCursorX','devModeCursorY'].forEach(function(k) {
                sessionStorage.removeItem(k);
            });
        });
    }

    if (sessionStorage.getItem('devMode') === '1') {
        applyDevModeVisuals(false);
    }

    function navigateBrandHome() {
        if (brand.href && brand.href !== window.location.href) {
            window.location.assign(brand.href);
        }
    }

    var clickCount = 0;
    var clickTimer = null;
    brand.addEventListener('click', function(e) {
        if (!isAdminUser || sessionStorage.getItem('devMode') === '1') return;

        e.preventDefault();
        clickCount++;
        clearTimeout(clickTimer);
        clickTimer = setTimeout(function() {
            if (clickCount > 0) {
                navigateBrandHome();
            }
            clickCount = 0;
        }, 800);

        if (clickCount >= 10) {
            clickCount = 0;
            clearTimeout(clickTimer);
            sessionStorage.setItem('devMode', '1');
            applyDevModeVisuals(true);
        }
    });
});
