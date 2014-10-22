using AutoSimulator.Properties;
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using Excel = Microsoft.Office.Interop.Excel;

namespace AutoSimulator
{
	class TestResult
	{
		public float TestParam { get; set; }

		public float Throughput { get; set; }
		public float Throughput_leftInterval { get; set; }
		public float Throughput_rightInverval { get; set; }

		public float Delay { get; set; }
		public float Delay_leftInterval { get; set; }
		public float Delay_rightInverval { get; set; }
	}

	class Program
	{
		const String PYTHON_MAIN = "psim.py";
		static String s_pathToMainPython = null;
		static String PathToMainPython
		{
			get
			{
				if(s_pathToMainPython == null)
				{
					s_pathToMainPython = FindFile(	new List<String>() 
													{
														Settings.Default.SimulatorDir, 
														Environment.CurrentDirectory 
													},
													PYTHON_MAIN);
					if (s_pathToMainPython == null)
					{
						throw new InvalidOperationException("could not find : " + PYTHON_MAIN);
					}
				}
				return s_pathToMainPython;
			}
		}

		const String OUTPUT_DATA_FOLDER = "OutputData";
		static String s_outputDataPath = null;
		static String OutputDataPath
		{
			get
			{
				if(s_outputDataPath == null)
				{
					s_outputDataPath = FindFile(	new List<String>() 
													{
														Settings.Default.SimulatorDir, 
														Environment.CurrentDirectory 
													}, 
													OUTPUT_DATA_FOLDER, true);
					if (s_outputDataPath == null)
					{
						throw new InvalidOperationException("Could not find output data directory! : " + OUTPUT_DATA_FOLDER);
					}
					s_outputDataPath += @"\";
				}
				return s_outputDataPath;
			}
		}

		static String FindFile(IEnumerable<String> dirs, string target, bool isDirectory = false)
		{
			String result = null;
			foreach(var dir in dirs)
			{
				result = FindPath(dir, target, isDirectory);
				if(result != null)
				{
					break;
				}
			}

			return result;
		}

		static String FindPath(string dir, string target, bool isDirectory = false)
		{
			String path = null;
			if (!isDirectory)
			{
				path = (from file in Directory.GetFiles(dir)
						where file.Contains(target)
						select file).FirstOrDefault();
			}
			else
			{
				path = (from file in Directory.GetDirectories(dir)
						where file.Contains(target)
						select file).FirstOrDefault();
			}

			if(path == null)
			{
				var parentDir = Directory.GetParent(dir);
				if (parentDir != null)
				{
					path = FindPath(parentDir.FullName, target);
				}
			}

			return path;
		}

		static TestResult RunTest(String protocolType, int stationCount, float probability, int simulationTime, int trials, IEnumerable<int> seeds)
		{
			TestResult testResults = new TestResult();

			var pythonArgs =	" " + protocolType +
								" " + stationCount + 
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

			rawResults = rawResults.Replace('\r', ' ');
			var lines = rawResults.Split('\n');
			// line 2 is throughput + confidence
			// line 3 is delay + confidence
			var line2 = lines[1];
			var line3 = lines[2];

			var words = line2.Split(' ');
			testResults.Throughput = float.Parse(words[0]);
			var throughputStd = float.Parse(words[1]);
			testResults.Throughput_leftInterval = testResults.Throughput - throughputStd;
			testResults.Throughput_rightInverval = testResults.Throughput + throughputStd;

			words = line3.Split(' ');
			testResults.Delay = float.Parse(words[0]);
			var delayStd = float.Parse(words[1]);
			testResults.Delay_leftInterval = testResults.Delay - delayStd;
			testResults.Delay_rightInverval = testResults.Delay + delayStd;

			return testResults;
		}

		static void Main(string[] args)
		{
			var t1 = Task.Factory.StartNew(() =>
			{
				VariedProbability();
			});
			var t2 = Task.Factory.StartNew(() =>
			{
				VariedStationCount(0.001F);
			});
			var t3 = Task.Factory.StartNew(() =>
			{
				VariedStationCount(0.01F);
			});
			var t4 = Task.Factory.StartNew(() =>
			{
				VariedStationCount(0.1F);
			});

			t1.Wait();
			t2.Wait();
			t3.Wait();
			t4.Wait();
		}

		static void OutputResults(String fileName, string paramName, List<TestResult> results)
		{
			const int Param_col = 1;

			const int Throughput_col = 3;
			const int Throughput_left_col = 4;
			const int Throughput_right_col = 5;

			const int averageDelay_col = 7;
			const int averageDelay_left_col = 8;
			const int averageDelay_right_col = 9;

			Excel.Application xlApp = new Excel.Application();
			Excel.Workbook xlWorkBook = xlApp.Workbooks.Add();
			Excel.Worksheet xlWorkSheet = xlWorkBook.Worksheets.get_Item(1);

			xlApp.DisplayAlerts = false;
			xlApp.AlertBeforeOverwriting = false;

			results.Sort((left, right) => left.TestParam.CompareTo(right.TestParam));

			// first write in the headers
			{
				xlWorkSheet.Cells[1, Param_col] = paramName;

				xlWorkSheet.Cells[1, Throughput_col] = "Throughput";
				xlWorkSheet.Cells[1, Throughput_left_col] = "Throughput Left Interval";
				xlWorkSheet.Cells[1, Throughput_right_col] = "Throughput Right Interval";

				xlWorkSheet.Cells[1, averageDelay_col] = "Average Delay Per Frame";
				xlWorkSheet.Cells[1, averageDelay_left_col] = "Average Delay Per Frame Left Interval";
				xlWorkSheet.Cells[1, averageDelay_right_col] = "Average Delay Per Frame Right Interval";
			}

			// now write each element row by row
			int rowNum = 2;
			foreach (var res in results)
			{
				xlWorkSheet.Cells[rowNum, Param_col] = res.TestParam;

				xlWorkSheet.Cells[rowNum, Throughput_col] = res.Throughput;
				xlWorkSheet.Cells[rowNum, Throughput_left_col] = res.Throughput_leftInterval;
				xlWorkSheet.Cells[rowNum, Throughput_right_col] = res.Throughput_rightInverval;

				xlWorkSheet.Cells[rowNum, averageDelay_col] = res.Delay;
				xlWorkSheet.Cells[rowNum, averageDelay_left_col] = res.Delay_leftInterval;
				xlWorkSheet.Cells[rowNum, averageDelay_right_col] = res.Delay_rightInverval;

				++rowNum;
			}

			object misValue = System.Reflection.Missing.Value;

			xlWorkBook.SaveAs(OutputDataPath + fileName);
			xlWorkBook.Close();
			xlApp.Quit();

			ReleaseComObject(xlWorkSheet);
			ReleaseComObject(xlWorkBook);
			ReleaseComObject(xlApp);
		}

		static void ReleaseComObject(object obj)
		{
			try
			{
				System.Runtime.InteropServices.Marshal.ReleaseComObject(obj);
				obj = null;
			}
			catch (Exception ex)
			{
				obj = null;
				Console.WriteLine("Exception Occurred while releasing object " + ex.ToString());
			}
			finally
			{
				GC.Collect();
			}
		}

#region Tests

		const int SLOT_TIME = 10000;
		const int TRIAL_COUNT = 10;
		const int NUMBER_OF_TESTS = 50;

		public static void VariedProbability()
		{
			const int STATIONS = 20;
			var SEEDS = Enumerable.Range(1, TRIAL_COUNT);

			const float PROBABILITY_START = 0.0F;
			const float PROBABILITY_END = 0.15F;

			Dictionary<String, List<TestResult>> results = new Dictionary<string,List<TestResult>>()
			{
				{ "T", new List<TestResult>() },
				{ "P", new List<TestResult>() },
				{ "I", new List<TestResult>() },
				{ "B", new List<TestResult>() }
			};

			foreach(var protToTest in results)
			{
				List<TestResult> currentRun = new List<TestResult>();
				for (int testNum = 0; testNum < NUMBER_OF_TESTS; ++testNum )
				{
					float probability = PROBABILITY_START + (float)(testNum) / NUMBER_OF_TESTS * PROBABILITY_END;
					var res = RunTest(protToTest.Key, STATIONS, probability, SLOT_TIME, TRIAL_COUNT, SEEDS);
					res.TestParam = probability;
					currentRun.Add(res);

					System.Console.WriteLine("Test : " + testNum + " / " + NUMBER_OF_TESTS + " completed!");
				}

				OutputResults("VariedProbability_" + protToTest.Key, "Probability", currentRun);
			}
		}

		public static void VariedStationCount(float probability)
		{
			var SEEDS = Enumerable.Range(1, TRIAL_COUNT);

			const int STATION_START = 2;
			const int STATION_END = 100;

			Dictionary<String, List<TestResult>> results = new Dictionary<string, List<TestResult>>()
			{
				{ "T", new List<TestResult>() },
				{ "P", new List<TestResult>() },
				{ "I", new List<TestResult>() },
				{ "B", new List<TestResult>() }
			};

			foreach (var protToTest in results)
			{
				List<TestResult> currentRun = new List<TestResult>();
				for (int testNum = 0; testNum < NUMBER_OF_TESTS; ++testNum)
				{
					int stations = (int)(STATION_START + (float)(testNum) / NUMBER_OF_TESTS * STATION_END);
					var res = RunTest(protToTest.Key, stations, probability, SLOT_TIME, TRIAL_COUNT, SEEDS);
					res.TestParam = stations;
					currentRun.Add(res);

					System.Console.WriteLine("Test : " + testNum + " / " + NUMBER_OF_TESTS + " completed!");
				}

				OutputResults("VariedStations_" + "_p_" + probability.ToString("0.000") + "_" + protToTest.Key + ".xlsx", "Stations", currentRun);
			}
		}
#endregion
	}
}
