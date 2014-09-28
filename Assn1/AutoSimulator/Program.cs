using AutoSimulator.Properties;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;

namespace AutoSimulator
{
	class TestResults
	{
		public float Throughput { get; set; }
		public float Throughput_leftInterval { get; set; }
		public float Throughput_rightInverval { get; set; }

		public float TransmissionPerFrame { get; set; }
		public float TransmissionPerFrame_leftInterval { get; set; }
		public float TransmissionPerFrame_rightInverval { get; set; }
	}

	class Program
	{
		const String PYTHON_MAIN = "main.py";

		static String s_pathToMainPython = null;
		static String PathToMainPython
		{
			get
			{
				if(s_pathToMainPython == null)
				{
					s_pathToMainPython = FindPythonMain(Environment.CurrentDirectory);
					if(s_pathToMainPython == null)
					{
						throw new InvalidOperationException("could not find : " + PYTHON_MAIN);
					}
				}
				return s_pathToMainPython;
			}
		}

		const  String TransmissionRegex = @"average of (?<average>\d*\.\d*) transmissions [^\[\]]*\[(?<leftInterval>\d*\.\d*),(?<rightIntverval>\d*\.\d*)\]";
		const String ThroughputRegex = @"average throughput of (?<average>\d*\.\d*) bits/time_unit [^\[\]]*\[(?<leftInterval>\d*\.\d*),(?<rightIntverval>\d*\.\d*)\]";

		static String FindPythonMain(string dir)
		{
			var path =	(from file in Directory.GetFiles(dir)
						where file.Contains(PYTHON_MAIN)
						select file).FirstOrDefault();

			if(path == null)
			{
				var parentDir = Directory.GetParent(dir);
				if (parentDir != null)
				{
					path = FindPythonMain(parentDir.FullName);
				}
			}

			return path;
		}

		static TestResults RunTest(int feedbackTime, int blockCount, int frameSize, double probability, int simulationTime, int trials, List<int> seeds)
		{
			TestResults testResults = new TestResults();

			var pythonArgs =	" " + feedbackTime + 
								" " + blockCount + 
								" " + frameSize + 
								" " + probability + 
								" " + simulationTime +
								" " + trials + 
								" " + String.Join(" ", seeds);

			Process testProc = new Process
			{
				StartInfo =
				{
					FileName = Settings.Default.PathToPython,
					Arguments = PathToMainPython + pythonArgs,
					RedirectStandardOutput = true,
					UseShellExecute = false
				}
			};
			testProc.Start();
			var rawResults = testProc.StandardOutput.ReadToEnd();
			testProc.WaitForExit();

			var match = Regex.Match(rawResults, TransmissionRegex, RegexOptions.Compiled);
			testResults.TransmissionPerFrame = float.Parse(match.Groups["average"].ToString());
			testResults.TransmissionPerFrame_leftInterval = float.Parse(match.Groups["leftInterval"].ToString());
			testResults.TransmissionPerFrame_rightInverval = float.Parse(match.Groups["rightIntverval"].ToString());

			match = Regex.Match(rawResults, ThroughputRegex, RegexOptions.Compiled);
			testResults.Throughput = float.Parse(match.Groups["average"].ToString());
			testResults.Throughput_leftInterval = float.Parse(match.Groups["leftInterval"].ToString());
			testResults.Throughput_rightInverval = float.Parse(match.Groups["rightIntverval"].ToString());

			return testResults;
		}

		static void Main(string[] args)
		{
			var res = RunTest(50, 1, 4000, 0.0005, 5000, 50, new List<int>(){ 5, 10, 15, 20 });
		}
	}
}
