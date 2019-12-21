using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using System.IO;
using System.Drawing;

namespace BrainSelector
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        List<string> fileEntries = new List<string>();
        int pos = 0;
        public MainWindow()
        {
            InitializeComponent();

            fileEntries = Directory.GetFiles(@"E:\Projects\COD Head Spotter\Raw Data").ToList();

            List<string> directoriedToCreate = new List<string>();

            // create all directories
            for (int col = 0; col < 10; col++)
            {
                for (int row = 0; row < 10; row++)
                {
                    directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Train\COL{col}-ROW{row}");
                    directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Validation\COL{col}-ROW{row}");
                }
            }

            directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Train\Neutral");
            directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Train\Unknown");
            directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Validation\Neutral");
            directoriedToCreate.Add($@"E:\Projects\COD Head Spotter\TrainingData\Validation\Unknown");

            foreach (string directory in directoriedToCreate)
            {
                if (!Directory.Exists(directory))
                {
                    Directory.CreateDirectory(directory);
                }
            }

            LoadInImage();
        }

        public void LoadInImage()
        {
            if (fileEntries.Count() > 0)
            {
                string target = fileEntries[0];

                MemoryStream ms = new MemoryStream();
                BitmapImage bi = new BitmapImage();

                byte[] arrbytFileContent = File.ReadAllBytes(target);
                ms.Write(arrbytFileContent, 0, arrbytFileContent.Length);
                ms.Position = 0;
                bi.BeginInit();
                bi.StreamSource = ms;
                bi.EndInit();
                ImageControl.Source = bi;
            }
            else
            {
                MessageBox.Show("No Image To Load");
            }
        }

        public void MoveThisImageTo(string target)
        {
            string OldSource = fileEntries[0];
            File.Move(OldSource, $@"{target}\{System.IO.Path.GetFileName(OldSource)}");
        }

        int count = 0;

        public void MoveAndLoadNextImage(string target)
        {
            MoveThisImageTo(target);
            fileEntries.RemoveAt(0);
            LoadInImage();
            count++;
            CountLabel.Content = $@"Count: {count}";
        }

        private void Grid_OnPreviewMouseLeftButtonDown(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            if (e.ClickCount == 2) // for double-click, remove this condition if only want single click
            {
                var point = Mouse.GetPosition(myGrid);

                int row = 0;
                int col = 0;
                double accumulatedHeight = 0.0;
                double accumulatedWidth = 0.0;

                // calc row mouse was over
                foreach (var rowDefinition in myGrid.RowDefinitions)
                {
                    accumulatedHeight += rowDefinition.ActualHeight;
                    if (accumulatedHeight >= point.Y)
                        break;
                    row++;
                }

                // calc col mouse was over
                foreach (var columnDefinition in myGrid.ColumnDefinitions)
                {
                    accumulatedWidth += columnDefinition.ActualWidth;
                    if (accumulatedWidth >= point.X)
                        break;
                    col++;
                }

                // row and col now correspond Grid's RowDefinition and ColumnDefinition mouse was 
                // over when double clicked!

                RowLabel.Content = $@"Row: {row}";
                ColLabel.Content = $@"Column: {col}";

                string TargetDirectory = $@"E:\Projects\COD Head Spotter\TrainingData\Train\COL{col}-ROW{row}";

                MoveAndLoadNextImage(TargetDirectory);
            }
        }

        private void ShowGridCheckBox_Checked(object sender, RoutedEventArgs e)
        {
            myGrid.ShowGridLines = true;
        }

        private void ShowGridCheckBox_Unchecked(object sender, RoutedEventArgs e)
        {
            myGrid.ShowGridLines = false;
        }

        private void Neutral_Click(object sender, RoutedEventArgs e)
        {
            MoveAndLoadNextImage($@"E:\Projects\COD Head Spotter\TrainingData\Train\Neutral");
        }

        private void UnknownButton_Click(object sender, RoutedEventArgs e)
        {
            MoveAndLoadNextImage($@"E:\Projects\COD Head Spotter\TrainingData\Train\Unknown");
        }

        private void Button_Click(object sender, RoutedEventArgs e)
        {
            List<string> Sources = new List<string>();

            List<string> Destinations = new List<string>();

            for (int col = 0; col < 10; col++)
            {
                for (int row = 0; row < 10; row++)
                {
                    Sources.Add($@"E:\Projects\COD Head Spotter\TrainingData\Train\COL{col}-ROW{row}");
                    Destinations.Add($@"E:\Projects\COD Head Spotter\TrainingData\Validation\COL{col}-ROW{row}");
                }
            }

            for(int i =0;i<Sources.Count();i++)
            {

                List<string> sourceFiles = Directory.GetFiles(Sources[i]).ToList();

                if (sourceFiles.Count > 3)
                {
                    File.Move(sourceFiles[0], $@"{Destinations[i]}\{System.IO.Path.GetFileName(sourceFiles[0])}");
                }
            }


        }
    }
}
