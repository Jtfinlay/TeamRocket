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
	class TestResults
	{
		public float TestParam { get; set; }

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

		const String OUTPUT_DATA_FOLDER = "OutputData";
		static String s_outputDataPath = null;
		static String OutputDataPath
		{
			get
			{
				if(s_outputDataPath == null)
				{
					s_outputDataPath = FindOutputDataPath(Environment.CurrentDirectory);
					if (s_outputDataPath == null)
					{
						throw new InvalidOperationException("Could not find output data directory! : " + OUTPUT_DATA_FOLDER);
					}
					s_outputDataPath += @"\";
				}
				return s_outputDataPath;
			}
		}

		const String TransmissionRegex = @"average of (?<average>-*\d*\.\d*\S*) transmissions [^\[\]]*\[(?<leftInterval>-*\d*\.\d*\S*),(?<rightIntverval>-*\d*\.\d*\S*)\]";
		const String ThroughputRegex = @"average throughput of (?<average>-*\d*\.\d*\S*) bits/time_unit [^\[\]]*\[(?<leftInterval>-*\d*\.\d*\S*),(?<rightIntverval>-*\d*\.\d*\S*)\]";

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

		static String FindOutputDataPath(string dir)
		{
			var path = (from file in Directory.GetDirectories(dir)
						where file.Contains(OUTPUT_DATA_FOLDER)
						select file).FirstOrDefault();

			if (path == null)
			{
				var parentDir = Directory.GetParent(dir);
				if (parentDir != null)
				{
					path = FindOutputDataPath(parentDir.FullName);
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
			
			var t1 = Task.Factory.StartNew(() =>
			{
				TestBlockSizeGreaterThanOne();
			});
			/*var t2 = Task.Factory.StartNew(() =>
			{
				TestBlockSizeZeroAndOne();
			});*/
			/*var t3 = Task.Factory.StartNew(() =>
			{
				TestThroughputWithRespectToProbability();
			});*/

			t1.Wait();
			//t2.Wait();
			//t3.Wait();
		}

		static void OutputResults(String fileName, string paramName, List<TestResults> results)
		{
			const int Param_col = 1;

			const int Throughput_col = 3;
			const int Throughput_left_col = 4;
			const int Throughput_right_col = 5;

			const int averageTransmissions_col = 7;
			const int averageTransmissions_left_col = 8;
			const int averageTransmissions_right_col = 9;

			Excel.Application xlApp = new Excel.Application();
			Excel.Workbook xlWorkBook = xlApp.Workbooks.Add();
			Excel.Worksheet xlWorkSheet = xlWorkBook.Worksheets.get_Item(1);

			xlApp.DisplayAlerts = false;
			xlApp.AlertBeforeOverwriting = false;

			results.Sort((left, right) =>  left.TestParam.CompareTo(right.TestParam) );

			// first write in the headers
			{
				xlWorkSheet.Cells[1, Param_col] = paramName;

				xlWorkSheet.Cells[1, Throughput_col] = "Throughput";
				xlWorkSheet.Cells[1, Throughput_left_col] = "Throughput Left Interval";
				xlWorkSheet.Cells[1, Throughput_right_col] = "Throughput Right Interval";

				xlWorkSheet.Cells[1, averageTransmissions_col] = "Average Transmissions Per Frame";
				xlWorkSheet.Cells[1, averageTransmissions_left_col] = "Average Transmissions Per Frame Left Interval";
				xlWorkSheet.Cells[1, averageTransmissions_right_col] = "Average Transmissions Per Frame Right Interval";
			}

			// now write each element row by row
			int rowNum = 2;
			foreach (var res in results)
			{
				xlWorkSheet.Cells[rowNum, Param_col] = res.TestParam;

				xlWorkSheet.Cells[rowNum, Throughput_col] = res.Throughput;
				xlWorkSheet.Cells[rowNum, Throughput_left_col] = res.Throughput_leftInterval;
				xlWorkSheet.Cells[rowNum, Throughput_right_col] = res.Throughput_rightInverval;

				xlWorkSheet.Cells[rowNum, averageTransmissions_col] = res.TransmissionPerFrame;
				xlWorkSheet.Cells[rowNum, averageTransmissions_left_col] = res.TransmissionPerFrame_leftInterval;
				xlWorkSheet.Cells[rowNum, averageTransmissions_right_col] = res.TransmissionPerFrame_rightInverval;

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

#region Varying Block-size > 1
		static void TestBlockSizeGreaterThanOne()
		{
			const int START_BLOCK_COUNT = 1;
			const int END_BLOCK_COUNT = 500;
			const int BLOCK_COUNT_STEP = 1;

			const int FEEDBACK_TIME = 500;
			const int FRAME_SIZE = 4000;
			const float PROBABILITY = 0.0005F;
			const int SIMULATION_TIME = 50000;
			const int TRIALS = 500;
			List<int> SEEDS = Enumerable.Range(0, TRIALS).ToList<int>();

			List<TestResults> results = new List<TestResults>();

			for(int blockCount = START_BLOCK_COUNT; blockCount < END_BLOCK_COUNT ; blockCount += BLOCK_COUNT_STEP)
			{
				if(FRAME_SIZE % blockCount == 0)
				{

					var res = RunTest(FEEDBACK_TIME, blockCount, FRAME_SIZE, PROBABILITY, SIMULATION_TIME, TRIALS, SEEDS);
					res.TestParam = blockCount;
					results.Add(res);
				}
			}

			OutputResults("test_blockSizeGreaterThanOne", "BlockCount", results);
		}
#endregion

		#region Compare block size zero and one
		static void TestBlockSizeZeroAndOne()
		{
			const int ZERO_BLOCK_SIZE = 0;
			const int ONE_BLOCK_SIZE = 1;

			const float PROBABILITY_START = 0.000500F;
			const float PROBABILITY_END =	0.000005F;
			const float PROBABILITY_STEP = (PROBABILITY_START - PROBABILITY_END) / 50;

			const int FEEDBACK_TIME = 500;
			const int FRAME_SIZE = 4000;
			const int SIMULATION_TIME = 50000;
			const int TRIALS = 300;
			List<int> SEEDS = Enumerable.Range(0, TRIALS).ToList<int>();

			List<TestResults> results = new List<TestResults>();

			for (float probability = PROBABILITY_START; probability > PROBABILITY_END; probability -= PROBABILITY_STEP)
			{
				var res = RunTest(FEEDBACK_TIME, ZERO_BLOCK_SIZE, FRAME_SIZE, probability, SIMULATION_TIME, TRIALS, SEEDS);
				res.TestParam = probability;
				results.Add(res);
			}

			OutputResults("test_blockSizeZero", "probability", results);
			results = new List<TestResults>();

			for (float probability = PROBABILITY_START; probability > PROBABILITY_END; probability -= PROBABILITY_STEP)
			{
				var res = RunTest(FEEDBACK_TIME, ONE_BLOCK_SIZE, FRAME_SIZE, probability, SIMULATION_TIME, TRIALS, SEEDS);
				res.TestParam = probability;
				results.Add(res);
			}

			OutputResults("test_blockSizeOne", "probability", results);
			results = new List<TestResults>();

			for (float probability = PROBABILITY_START; probability > PROBABILITY_END; probability -= PROBABILITY_STEP)
			{
				var res = RunTest(FEEDBACK_TIME, 20, FRAME_SIZE, probability, SIMULATION_TIME, TRIALS, SEEDS);
				res.TestParam = probability;
				results.Add(res);
			}

			OutputResults("test_blockSizeTwenty", "probability", results);
			results = new List<TestResults>();

			for (float probability = PROBABILITY_START; probability > PROBABILITY_END; probability -= PROBABILITY_STEP)
			{
				var res = RunTest(FEEDBACK_TIME, 80, FRAME_SIZE, probability, SIMULATION_TIME, TRIALS, SEEDS);
				res.TestParam = probability;
				results.Add(res);
			}

			OutputResults("test_blockSizeEighty", "probability", results);
		}
		#endregion

		#region Compare block size zero and one
		static void TestThroughputWithRespectToProbability()
		{	
			const float PROBABILITY_START = 0.001500F;
			const float PROBABILITY_END =	0.000005F;
			const float PROBABILITY_STEP = (PROBABILITY_START - PROBABILITY_END) / 100;

			const int BLOCK_SIZE = 4;
			const int FEEDBACK_TIME = 500;
			const int FRAME_SIZE = 4000;
			const int SIMULATION_TIME = 50000;
			const int TRIALS = 500;
			List<int> SEEDS = Enumerable.Range(0, TRIALS).ToList<int>();

			List<TestResults> results = new List<TestResults>();

			for (float probability = PROBABILITY_START; probability > PROBABILITY_END; probability -= PROBABILITY_STEP)
			{
				var res = RunTest(FEEDBACK_TIME, BLOCK_SIZE, FRAME_SIZE, probability, SIMULATION_TIME, TRIALS, SEEDS);
				res.TestParam = probability;
				results.Add(res);
			}

			OutputResults("test_throughput", "probability", results);
		}
		#endregion


#endregion
	}
}
