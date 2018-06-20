# Banana-Plot
Graphical interface for plotting contour ("Banana") plots of aerosol size distribution from TSI SMPS data output

# Directions for use

Output size distribution from TSI Aerosol Instrument Manager (AIM) in dN/dlogDp format using comma-delimited rows

Run Contour-GUI.pyw

Load in AIM output file using File -> Open (If this step is skipped, program will prompt user to open file when "Make Banana Plot" is clicked)

You can choose between using the entire file or a specific time range in the output file.

Click "Make Banana Plot." The program will automatically display the plot it created as well as saves a .png in the local directory. The plot will have the option to zoom and save as needed.

# Dependencies

Matplotlib
Numpy
