close all; 
clear all;
clc

data = csvread('wage.csv');
inputData = [data(1:600,1:3),data(1:600,4)];
j = 10;
mseSum = 0;
madSum = 0;
k1 = [inputData(1:30,:); inputData(300:330,:)];
k2 = [inputData(31:60,:); inputData(331:360,:)];
k3 = [inputData(61:90,:); inputData(361:390,:)];
k4 = [inputData(91:120,:); inputData(391:420,:)];    
k5 = [inputData(121:150,:); inputData(421:450,:)];
k6 = [inputData(151:180,:); inputData(451:480,:)];
k7 = [inputData(181:210,:); inputData(481:510,:)];
k8 = [inputData(211:240,:); inputData(511:540,:)];
k9 = [inputData(241:270,:); inputData(541:570,:)];
k10 = [inputData(271:300,:); inputData(571:600,:)];
for i=1:j
    if i == 1
        trainMatrix = [k1;k2;k3;k4;k5;k6;k7;k8;k9];
        testMatrix = k10;
    end
    if i == 2
        trainMatrix = [k1;k2;k3;k4;k5;k6;k7;k8;k10];
        testMatrix = k9;
    end
    if i == 3
        trainMatrix = [k1;k2;k3;k4;k5;k6;k7;k9;k10];
        testMatrix = k8;
    end
    if i == 4
        trainMatrix = [k1;k2;k3;k4;k5;k6;k8;k9;k10];
        testMatrix = k7;
    end
     if i == 5
        trainMatrix = [k1;k2;k3;k4;k5;k7;k8;k9;k10];
        testMatrix = k6;
     end
      if i == 6
        trainMatrix = [k1;k2;k3;k4;k6;k7;k8;k9;k10];
        testMatrix = k5;
      end
       if i == 7
        trainMatrix = [k1;k2;k3;k5;k6;k7;k8;k9;k10];
        testMatrix = k4;
       end
     if i == 8
        trainMatrix = [k1;k2;k4;k5;k6;k7;k8;k9;k10];
        testMatrix = k3;
     end
      if i == 9
        trainMatrix = [k1;k3;k4;k5;k6;k7;k8;k9;k10];
        testMatrix = k2;
      end
       if i == 10
        trainMatrix = [k2;k3;k4;k5;k6;k7;k8;k9;k10];
        testMatrix = k1;
       end
       inputTrain = trainMatrix(:,1:3);
       disp('train matrix:')
       disp(trainMatrix)
       target = trainMatrix(:,4);
       
       inputTrain = inputTrain';
       outputTrain = target'; 
       
       disp('inputtrain matrix:')
       disp(inputTrain)
       disp('outputtrain matrix:')                               
       lr = maxlinlr(inputTrain);
       net = newlin(inputTrain,outputTrain,0,lr);
       
       disp('Neurono bias reiksme:');
       disp(net.b{1});
       disp('Neurono svorio koeficientai:');
       disp(net.IW{1});
       
       net.trainParam.goal = 0.01;
       net.trainParam.epochs = 1000;
       net.layers{1}.transferFcn = 'purelin';
       net = train(net, inputTrain, outputTrain);
       
       disp('Neurono bias reiksme:');
       disp(net.b{1});
       disp('Neurono svorio koeficientai:');
       
       disp(net.IW{1});
       inputTest = testMatrix(:,1:3); %(15x4)
       targetTest = testMatrix(:,4);
       inputTest = inputTest'; %(4x15)
       outputTest = targetTest'; %(3x15)
       
       result = sim(net, inputTest);
       
       e = outputTest - result;
       
       mseSum = mseSum + mse(e)
       madSum = madSum + mad(e)
       view(net)
       disp(result)
       disp(outputTest)
end
avgTest=avgTest/10;
mseAvg = mseSum / 10;
madAvg = madSum / 10;
disp(['Mean-Square-Error, MSE:', num2str(mseAvg)]);
disp(['Median absolute Deviation, MAD:', num2str(madAvg)]);
disp(['network hit average (kfold = 10):', num2str(avgTest)]);