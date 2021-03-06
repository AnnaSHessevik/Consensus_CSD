//Slightly modified version of FindCorrAndVar.cpp by André Voigt from the conventional CSD approach (https://github.com/andre-voigt/CSD)
//Run this before FindCSD.cpp . Run it once on each data set for which you want to find correlations. Correlation and variance is output to RhoAndVar.txt - remember to rename the file before running the next iteration, or your original data will be overwritten. If you want to run the computations for each file in parallel, make a separate folder for each data set, copy this code to that folder and compile there. 

#include <ctime>
#include <stdio.h>
#include <cmath>
#include <iostream>
#include <list>
#include <fstream>
#include <cstring>
#include <stdlib.h>


using namespace std;


//Parameters depending on input file

const char* expDataFile = "sorted_not_sun_1000genes.txt"; //Name of expression data file
const char* outFile = "spearman_not_sun_1000genes.txt"; //Name of output data file
int sampleSize = 14; //Number of data points per gene (normally number of individuals from which data is collected, corresponds to columns in the expression data text file)
const int numberOfGenes = 1000;// Number of distinct genes for which there is expression data (corresponds to rows in expression data)
const int subSampleSize = 8;// of subsamples for determination of variance in co-expression. 10 is a good minimum - can be increased if sampleSize is very large.                                                                      


struct Pair;


struct Pair
{
  double x;
  double y;
  double xRank;
  double yRank;
};



double spearman(list<Pair> subSample);

int main(int argc, char* argv[])
{
	//Modification
	if (argc  == 4){ //program name, name of input file, name of output file, sample size. Note that number of genes are constant
		expDataFile = argv[1];
		outFile = argv[2];
		sampleSize = strtol(argv[3], NULL, 0);
	}
  srand(time(NULL));

  ifstream inStream;
  ofstream outStream;
  
  double expressionValues[sampleSize][numberOfGenes];
  string geneName[numberOfGenes];
  
  inStream.open(expDataFile);
  
  if(inStream.is_open())
    {
      char temp[4000000];
      int i = 0;
      while(!inStream.getline(temp, 4000000).eof() && i < numberOfGenes)
	{     
	  inStream >> geneName[i];

	  for (int k = 0; k < sampleSize; k++)
	    {
	      inStream >> expressionValues[k][i];

	    }

	  i++;
	}
      

    }
  


  int newSequence[sampleSize];
  bool alreadyTaken[sampleSize];
  for (int i = 0; i < sampleSize; i++)
    {
      alreadyTaken[i] = 0;
    }
  for (int i = 0; i < sampleSize; i++)
    {
      int r = rand() % sampleSize;
      while(alreadyTaken[r])
	{
	  r = rand() % sampleSize;
	}
      newSequence[i] = r;
      alreadyTaken[r] = 1;
    }

  double shuffledExpression[sampleSize][numberOfGenes];

  for (int i = 0; i < sampleSize; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  shuffledExpression[i][j] = expressionValues[newSequence[i]][j];
	}
    }
  for (int i = 0; i < sampleSize; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  expressionValues[i][j] = shuffledExpression[i][j];
	}
    }
  


  double corrcoefs[numberOfGenes][numberOfGenes];


  int selectionSequence[sampleSize][sampleSize];
  int table[sampleSize][sampleSize];

  for (int i = 0; i < sampleSize; i++)
    {
      for (int j = 0; j < sampleSize; j++)
	{
	  table[i][j] = 2;
	  selectionSequence[i][j] = 0;
	}
    }
  for (int i = 0; i < sampleSize; i++)
    {
      table[i][i] = 0;
    }
  
  int selection = 0;
  bool end = 0;

  int itr = 0; 
  int jtr = 0;
  int row;
  int col; 
  int nestlevel = 0;
  int fullSelections[numberOfGenes][numberOfGenes];
  for (int i = 0; i < numberOfGenes; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  fullSelections[i][j] = 0;
	}
    }
  
  int prevNodesID[subSampleSize];
  int nodeCounter;
  bool nodeIsOK;
  

  double corrcoefAverage[numberOfGenes][numberOfGenes];
  double corrcoefAverageFull[numberOfGenes][numberOfGenes];



  double corrcoefAverageSquare[numberOfGenes][numberOfGenes];
  double corrcoefVar[numberOfGenes][numberOfGenes];
  double squareDev[numberOfGenes][numberOfGenes];
  double sumSquareDev[numberOfGenes][numberOfGenes];
  double meanSquareDev[numberOfGenes][numberOfGenes];
  

  for (int i = 0; i < numberOfGenes; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  corrcoefAverage[i][j] = 0;
	  corrcoefAverageSquare[i][j] = 0;
	  corrcoefVar[i][j] = 0;
	  sumSquareDev[i][j] = 0;
	  list<Pair> completeSample;
	  for (int k = 0; k < sampleSize; k++)
	    {
	      Pair newPair;
	      newPair.x = expressionValues[k][i];
	      newPair.y = expressionValues[k][j];
	      completeSample.push_back(newPair);
	    }
	  corrcoefAverageFull[i][j] = spearman(completeSample);
	}
    }
  
  /*
  
  while(pow(subSampleSize,nestlevel) < sampleSize)

    {
      for (int i = 0; i < sampleSize; i = i + pow(subSampleSize,(nestlevel+1)))
	{
	  for (int j = 0; j < pow(subSampleSize,(2*nestlevel)); j++)
	    {

	      
	      
	      selection++;
	      nodeCounter = 0;

	      col = i + (j%int((pow(subSampleSize,nestlevel))));
	      row = i + (i+j-col)/(pow(subSampleSize,nestlevel));
	      prevNodesID[0] = row;
	      nodeCounter++;
	      
	      while (nodeCounter < subSampleSize && col < sampleSize)

		{
		  nodeIsOK = 1;
		  
		  if (table[row][col] != 2)
		    {
		      nodeIsOK = 0;
		    }
		  
		  for (int k = 0; k < nodeCounter; k++)
		    {
		      if (table[prevNodesID[k]][col] != 2)
			{
			  nodeIsOK = 0;
			}
		    }

		  if (nodeIsOK)
		    {
		      for (int k = 0; k < nodeCounter; k++)
			{
			  table[prevNodesID[k]][col] = 1;
			  table[col][prevNodesID[k]] = 1;
			  selectionSequence[prevNodesID[k]][col] = selection;
			}
		      
		      table[row][col] = 1;
		      table[col][row] = 1;
		      selectionSequence[row][col] = selection;
		      prevNodesID[nodeCounter] = col;
		      nodeCounter++;
		     
		      row = col;
		    }
		
		  

		  col++;
		}
	      
	      if (nodeCounter == subSampleSize)
		{

		  
		  //cout << "Sample number " << fullSelections << "\n";
		  Pair newPair;
		  for (int k = 0; k < numberOfGenes; k++)
		    {
		      //cout << k << "\n";
		      for (int l = k+1; l < numberOfGenes; l++)
			{
			  fullSelections[k][l]++;
			  fullSelections[l][k]++;
			  list<Pair> subSample;
			  for (int m = 0; m < subSampleSize; m++)
			    {
			      newPair.x = expressionValues[prevNodesID[m]][k];
			      newPair.y = expressionValues[prevNodesID[m]][l];
			      subSample.push_back(newPair);
			      //cout << k << "\t" << l << "\t" << m << "\n";
			    }
			  corrcoefs[k][l] = spearman(subSample);
			  if (!isnan(corrcoefs[k][l]))
			    {
			      //cout << corrcoefs[k][l] << "\n"; 
			      corrcoefAverage[k][l] = corrcoefAverage[k][l] + corrcoefs[k][l];
			      corrcoefAverageSquare[k][l] = corrcoefAverageSquare[k][l] + pow(corrcoefs[k][l], 2);
			 
			      squareDev[k][l] = pow(corrcoefAverageFull[k][l]-corrcoefs[k][l],2);
			      sumSquareDev[k][l] = sumSquareDev[k][l] + squareDev[k][l];


			  
			      corrcoefs[l][k] = corrcoefs[k][l];
			      corrcoefAverage[l][k] = corrcoefAverage[k][l];
			      corrcoefAverageSquare[l][k] = corrcoefAverageSquare[k][l];
			      squareDev[l][k] = squareDev[k][l];
			      sumSquareDev[l][k] = sumSquareDev[k][l];
			      //corrcoefs[k][l].push_back(spearman(subSample));
			      //cout << k << "\t" << l << "\t" << corrcoefs[k][l].back() <<"\n";
			      //~subSample();
			    }
			  else
			    {
			      fullSelections[k][l]--;
			      fullSelections[l][k]--;
			    }
			}     
		    }
		  //delete &newPair;
		}			  
	      
	      
	      //Reset if no full selection
	      if (nodeCounter < subSampleSize)
		{
		  for (int l = 2; l < nodeCounter; l++)
		    {
		      table[prevNodesID[0]][prevNodesID[l]] = 2;
		    }
		  
		  for (int k = 1; k < nodeCounter; k++)
		    {
		      for (int l = k+1; l < nodeCounter; l++)
			{
			  table[prevNodesID[k]][prevNodesID[l]] = 2;
			}	
		    }
		}
	    
	    }
	  
	}
    
      //cout << "LEVEL RAISE, SELECTION NUMBER " << selection << "\n";
      nestlevel++; 
    }
  
  //Compute mean and standard deviation
  
  for (int i = 0; i < numberOfGenes; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  //corrcoefAverage[i][j] = 0;
	  //corrcoefAverageSquare[i][j] = 0;
	  //for (list<double>::iterator it = corrcoefs[i][j].begin(); it != corrcoefs[i][j].end(); it++)
	  /*
	  for (int k = 1; k < fullSelections + 1; k++)
	    {
	      //corrcoefAverage[i][j] = corrcoefAverage[i][j] + (*it)/corrcoefs[i][j].size();
	      //corrcoefAverageSquare[i][j] = corrcoefAverageSquare[i][j] + pow((*it),2)/corrcoefs[i][j].size();
	      //corrcoefAverage[i][j] = corrcoefAverage[i][j] + corrcoefs[i][j][k]/fullSelections;
	      //corrcoefAverageSquare[i][j] = corrcoefAverageSquare[i][j] + pow(corrcoefs[i][j][k], 2)/fullSelections;
	    }
	  
	  corrcoefAverage[i][j] = corrcoefAverage[i][j] / double(fullSelections[i][j]);
	  corrcoefAverageSquare[i][j] = corrcoefAverageSquare[i][j] / double(fullSelections[i][j]);
	  corrcoefVar[i][j] = (corrcoefAverageSquare[i][j] - pow(corrcoefAverageFull[i][j],2))*(fullSelections[i][j])/(fullSelections[i][j]-1);
	  meanSquareDev[i][j] = sumSquareDev[i][j] / double(fullSelections[i][j]);
	}
    }
  
*/
  outStream.open(outFile);
  for (int i = 0; i < numberOfGenes; i++)
    {
      for (int j = 0; j < numberOfGenes; j++)
	{
	  outStream << geneName[i] << "\t" << geneName[j] << "\t" << corrcoefAverageFull[i][j] << "\t" << meanSquareDev[i][j] << "\n";
	}
    }

 outStream.close();

 outStream.open("RhoAndVarDetailed.txt");
 for (int i = 0; i < numberOfGenes; i++)
   {
     for (int j = 0; j < numberOfGenes; j++)
       {
	 outStream << geneName[i] << "\t" << geneName[j] << "\t" << corrcoefAverageFull[i][j] << "\t" << meanSquareDev[i][j] << "\t" << corrcoefAverage[i][j] << "\t" << fullSelections[i][j] << "\n";
       }
   }

 outStream.close();
   
 // outStream.open("SubsampleRho");

 // for (int i = 0; i < numberOfGenes; i++)
 //    {
 //      for (int j = 0; j < numberOfGenes; j++)
 // 	{
 // 	  outStream << geneName[i] << "\t" << geneName[j] << "\t" << corrcoefAverageFull[i][j] << "\t" << corrcoefAverage[i][j] << "\n";
 // 	}
 //    }


 // outStream.close();
}


double spearman(list<Pair> subSample)
{
  double xRank;
  double yRank;
  double xTies;
  double yTies;

  for (list<Pair>::iterator it = subSample.begin(); it != subSample.end(); it++)
    {
      xRank = 1;
      yRank = 1;
      xTies = -1;
      yTies = -1;
      for (list<Pair>::iterator jt = subSample.begin(); jt != subSample.end(); jt++)
	{
	  if ((*jt).x < (*it).x)
	    {
	      xRank++;
	    }
	  if ((*jt).x == (*it).x)
	    {
	      xTies++;
	    }

	  if ((*jt).y < (*it).y)
	    {
	      yRank++;
	    }
	  if ((*jt).y == (*it).y)
	    {
	      yTies++;
	    } 
	}
      
      (*it).xRank = xRank + xTies/2;
      (*it).yRank = yRank + yTies/2;
      //cout << xRank << "\t" << yRank << "\n";
    }
  double averageRank = (double(subSample.size())+1)/2;
  //cout << averageRank << "\n"; 

  double spearmanNum = 0;
  double spearmanDen1 = 0;
  double spearmanDen2 = 0;

  for (list<Pair>::iterator it= subSample.begin(); it != subSample.end(); it++)
    {
      spearmanNum = spearmanNum + ((*it).xRank-averageRank)*((*it).yRank-averageRank);
      spearmanDen1 = spearmanDen1 + pow(((*it).xRank-averageRank),2);
      spearmanDen2 = spearmanDen2 + pow(((*it).yRank-averageRank),2);
    }
  //cout << spearmanNum << "\t" << spearmanDen1 << "\t" << spearmanDen2 << "\n";
  spearmanDen1 = sqrt(spearmanDen1);
  spearmanDen2 = sqrt(spearmanDen2);
  
  return spearmanNum/(spearmanDen1*spearmanDen2);
  
  
  
}
