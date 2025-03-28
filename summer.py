import tkinter as tk
from datetime import datetime, timedelta
import pytz
import time

class WorldClockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("World Clock with DST Info")
        self.root.geometry("650x350")
        self.root.configure(bg='black')
        
        
        self.bg_color = 'black'
        self.text_colors = {
            'cet': '#00bfff',     # Deep Sky Blue
            'utc': '#00ff7f',     # Spring Green
            'unix': '#ff4500',    # Orange Red
            'status': '#9370db',  # Medium Purple
            'start': '#98fb98',   # Pale Green
            'end': '#ffa07a',     # Light Salmon
            'countdown': '#ff6347' # Tomato
        }
        
        # Create labels
        # Create labels with new color scheme
        self.label_cet = tk.Label(root, 
                                font=('Helvetica', 16, 'bold'),
                                fg=self.text_colors['cet'],
                                bg=self.bg_color)
        self.label_utc = tk.Label(root,
                                font=('Helvetica', 16, 'bold'),
                                fg=self.text_colors['utc'],
                                bg=self.bg_color)
        self.label_unix = tk.Label(root,
                                 font=('Helvetica', 16, 'bold'),
                                 fg=self.text_colors['unix'],
                                 bg=self.bg_color)
        self.label_summer_status = tk.Label(root,
                                          font=('Helvetica', 16, 'bold'),
                                          fg=self.text_colors['status'],
                                          bg=self.bg_color)
        self.label_summer_start = tk.Label(root,
                                         font=('Helvetica', 14),
                                         fg=self.text_colors['start'],
                                         bg=self.bg_color)
        self.label_summer_end = tk.Label(root,
                                       font=('Helvetica', 14),
                                       fg=self.text_colors['end'],
                                       bg=self.bg_color)
        self.label_next_change = tk.Label(root,
                                        font=('Helvetica', 14, 'bold'),
                                        fg=self.text_colors['countdown'],
                                        bg=self.bg_color)
        
        # Layout
        self.label_cet.pack(pady=8)
        self.label_utc.pack(pady=8)
        self.label_unix.pack(pady=8)
        self.label_summer_status.pack(pady=8)
        self.label_summer_start.pack(pady=8)
        self.label_summer_end.pack(pady=8)
        self.label_next_change.pack(pady=8)
        
        # Update immediately and start the timer
        self.update_time()
    
    def get_dst_dates(self, year):
        """Calculate DST start and end dates in CET for a given year"""
        # DST in CET starts last Sunday of March at 1:00 UTC (2:00 CET)
        dst_start = datetime(year, 3, 31, 1, tzinfo=pytz.utc)
        while dst_start.weekday() != 6:  # Sunday is 6
            dst_start -= timedelta(days=1)
        
        # DST ends last Sunday of October at 1:00 UTC (3:00 CEST -> 2:00 CET)
        dst_end = datetime(year, 10, 31, 1, tzinfo=pytz.utc)
        while dst_end.weekday() != 6:  # Sunday is 6
            dst_end -= timedelta(days=1)
            
        return (
            dst_start.astimezone(pytz.timezone('Europe/Berlin')),
            dst_end.astimezone(pytz.timezone('Europe/Berlin')))
        
    def update_time(self):
        # Get current times
        now_utc = datetime.now(pytz.utc)
        cet = pytz.timezone('Europe/Berlin')
        now_cet = now_utc.astimezone(cet)
        unix_time = int(time.time())
        
        # Check for summer time (DST)
        is_summer_time = now_cet.dst() != timedelta(0)
        summer_status = "ACTIVE" if is_summer_time else "NOT ACTIVE"
        
        # Get DST dates for current year
        dst_start, dst_end = self.get_dst_dates(now_cet.year)
        
        # Determine next DST change
        next_change = dst_start if now_cet < dst_start else dst_end
        if now_cet > dst_end:
            next_change = self.get_dst_dates(now_cet.year + 1)[0]
        
        time_until_change = next_change - now_cet
        days = time_until_change.days
        hours, remainder = divmod(time_until_change.seconds, 3600)
        minutes = remainder // 60
        
        # Update labels
        self.label_cet.config(text=f"CET Time: {now_cet.strftime('%Y-%m-%d %H:%M:%S')}")
        self.label_utc.config(text=f"UTC Time: {now_utc.strftime('%Y-%m-%d %H:%M:%S')}")
        self.label_unix.config(text=f"Unix Time: {unix_time}")
        self.label_summer_status.config(text=f"Daylight Saving Time Status: {summer_status}")
        self.label_summer_start.config(text=f"DST starts this year on: {dst_start.strftime('%Y-%m-%d %H:%M:%S')} +1 hour: 02:00 -> 03:00")
        self.label_summer_end.config(text=f"DST ends this year on: {dst_end.strftime('%Y-%m-%d %H:%M:%S')} -1 hour 03:00 -> 02:00")
        self.label_next_change.config(
            text=f"Next DST change in: {days} days, {hours} hours, {minutes} minutes",
            fg='red' if days < 30 else 'brown')
        
        # Schedule next update
        self.root.after(1000, self.update_time)

if __name__ == "__main__":
    root = tk.Tk()
    app = WorldClockApp(root)
    root.mainloop()
    


