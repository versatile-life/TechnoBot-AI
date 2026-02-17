def open_dashboard():

    root = tk.Tk()
    root.title("Factory Industrial Panel")
    root.attributes("-fullscreen", True)
    root.configure(bg="#101820")

    # ===== TOP BAR =====
    top = tk.Frame(root, bg="#1c1c1c", height=60)
    top.pack(fill="x")

    tk.Label(top, text="Worker ID:", fg="white", bg="#1c1c1c",
             font=("Arial", 14)).pack(side="left", padx=10)

    worker_entry = tk.Entry(top, font=("Arial", 14), width=15)
    worker_entry.pack(side="left")

    tk.Button(top, text="Logout",
              command=lambda: root.destroy(),
              bg="orange").pack(side="right", padx=20)

    # ===== MAIN AREA =====
    main = tk.Frame(root, bg="#101820")
    main.pack(fill="both", expand=True)

    # CAMERA FRAME
    cam_frame = tk.Frame(main, bg="#101820")
    cam_frame.pack(side="left", padx=20, pady=20)

    cam = cv2.VideoCapture(0)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)

    camera_label = tk.Label(cam_frame)
    camera_label.pack()

    def update_camera():
        try:
            ret, frame = cam.read()
            if ret:
                frame = cv2.resize(frame, (480, 270))
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                camera_label.imgtk = imgtk
                camera_label.configure(image=imgtk)
        except:
            pass

        camera_label.after(30, update_camera)  # slower refresh

    update_camera()

    def capture_issue():
        worker = worker_entry.get()
        if not worker:
            return
        ret, frame = cam.read()
        if ret:
            os.makedirs("issues", exist_ok=True)
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f"issues/{worker}_{timestamp}.jpg", frame)

    tk.Button(cam_frame, text="Capture Issue",
              font=("Arial", 14),
              command=capture_issue,
              bg="#333", fg="white").pack(pady=10)

    # CHAT FRAME
    chat_frame = tk.Frame(main, bg="#101820")
    chat_frame.pack(side="right", padx=20)

    chat = scrolledtext.ScrolledText(chat_frame,
                                     width=60,
                                     height=20,
                                     bg="#1e1e1e",
                                     fg="#00ff99",
                                     font=("Arial", 12))
    chat.pack()

    # BOTTOM BAR
    bottom = tk.Frame(root, bg="#1c1c1c", height=100)
    bottom.pack(fill="x")

    entry = tk.Entry(bottom, font=("Arial", 14), width=50)
    entry.pack(side="left", padx=20, pady=20)

    def ask():
        worker = worker_entry.get()
        text = entry.get()
        if not worker or not text:
            return

        response = smart_response(text)

        chat.insert(tk.END, f"{worker}: {text}\n")
        chat.insert(tk.END, f"Bot: {response}\n\n")

        try:
            threading.Thread(target=speak, args=(response,), daemon=True).start()
        except:
            pass

        entry.delete(0, tk.END)

    tk.Button(bottom, text="Send",
              font=("Arial", 14),
              command=ask,
              bg="#00aa88",
              fg="white").pack(side="left", padx=10)

    def emergency_alert():
        root.configure(bg="red")
        root.after(1000, lambda: root.configure(bg="#101820"))

    tk.Button(bottom, text="EMERGENCY",
              font=("Arial", 16),
              bg="red", fg="white",
              command=emergency_alert).pack(side="right", padx=20)

    def exit_fullscreen(event):
        root.attributes("-fullscreen", False)

    root.bind("<Escape>", exit_fullscreen)

    root.mainloop()
