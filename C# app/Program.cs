using System;
using System.IO;
using System.Windows.Forms;
using System.Windows.Forms.Integration;
using System.Windows.Controls;
using System.Runtime.InteropServices;

namespace Mp4Player
{
    public class ForcedVideoWindow : Form
    {
        private ElementHost _ctrlHost;
        private MediaElement _mediaPlayer;

        protected override bool ShowWithoutActivation => true;

        protected override CreateParams CreateParams
        {
            get
            {
                var cp = base.CreateParams;
                cp.ExStyle |= 0x80 | 0x8000000;
                return cp;
            }
        }

        public ForcedVideoWindow(string videoPath)
        {
            this.FormBorderStyle = FormBorderStyle.None;
            this.WindowState = FormWindowState.Maximized;
            this.StartPosition = FormStartPosition.Manual;
            this.BackColor = System.Drawing.Color.Black;
            
            this.ShowInTaskbar = false;
            
            this.TopMost = true; 

            this.Load += (s, e) => Cursor.Hide();

            try
            {
                _ctrlHost = new ElementHost { Dock = DockStyle.Fill };
                _mediaPlayer = new MediaElement
                {
                    Source = new Uri(videoPath),
                    LoadedBehavior = MediaState.Play,
                    UnloadedBehavior = MediaState.Manual,
                    Stretch = System.Windows.Media.Stretch.Uniform,
                    IsMuted = false
                };

                _mediaPlayer.MediaEnded += (s, e) =>
                {
                    _mediaPlayer.Stop();
                    _ctrlHost.Dispose();
                    this.Close();
                    Application.Exit();
                };

                _ctrlHost.Child = _mediaPlayer;
                this.Controls.Add(_ctrlHost);
            }
            catch
            {
                Application.Exit();
            }
        }

        protected override void Dispose(bool disposing)
        {
            if (disposing)
            {
                if (_mediaPlayer != null) _mediaPlayer.Stop();
                if (_ctrlHost != null) _ctrlHost.Dispose();
            }
            base.Dispose(disposing);
        }
    }

    class Program
    {
        [DllImport("kernel32.dll")]
        private static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [STAThread]
        static void Main(string[] args)
        {
            IntPtr consoleHandle = GetConsoleWindow();
            if (consoleHandle != IntPtr.Zero)
            {
                ShowWindow(consoleHandle, 0);
            }

            if (args.Length == 0) return;
            string videoPath = Path.GetFullPath(args[0]);
            if (!File.Exists(videoPath)) return;

            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);

            Application.Run(new ForcedVideoWindow(videoPath));
        }
    }
}
