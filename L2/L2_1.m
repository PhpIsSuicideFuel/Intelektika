clc, clear, close all;
load sunspot.txt;

%sunspot
%clear sunspot
%4:
figure(1);
plot(sunspot(:, 1), sunspot(:, 2), 'g-o');
grid on;
xlabel('Metai');
ylabel('Demiu skaicius');
title('Saules demiu aktyvumas 1700-2014 metais');
%5:
L = length(sunspot);
P = [sunspot(1:L-2, 2)'; sunspot(2:L-1, 2)'];
disp('P matrica:')
disp(P)
disp('P matricos dydis:')
size(P)
T = sunspot(3:L, 2)';
disp('T matrica:')
disp(T)
disp('T matricos dydis:')
size(T)
%6:
figure(2)
plot3(P(1,:), P(2,:), T, 'bo');
grid on;
xlabel('Saules demiu skaicius (n-2)-taisiais metais');
ylabel('Saules demiu skaicius (n-1)-taisiais metais');
zlabel('Saules demiu skaicius n-taisiais metais');
title('Saules demiu prognoziu, remiantis 2 ankstesniais metais, diagrama');
%7:
disp('Pu matrica:')
Pu = P(:, 1:200)
disp('Tu matrica:')
Tu = T(:, 1:200)
disp('Pu dydis:')
size(Pu)
disp('Tu dydis:')
size(Tu)
%8:
net = newlind(Pu, Tu);
%9:
disp('Neurono svorio koeficientai:');
disp(net.IW{1});
disp('Neurono bias reiksme:');
disp(net.b{1});
w1 = net.IW{1}(1);
w2 = net.IW{1}(2);
b = net.b{1};
%10:
Tsu = sim(net, Pu) 
figure(3), hold on;
plot(sunspot(3:202, 1), Tu, 'g-o');
plot(sunspot(3:202, 1), Tsu, 'b-o');
xlabel('Metai');
ylabel('Demiu skaicius');
grid on;
legend('Tikrosios demiu reiksmes', ...
    'Prognozuojamos demiu reiksmes');
title('Saules demiu prognozavimo kokybes patikrinimas 1702-1901 metams');
%11:
Ts = sim(net, P);
figure(4), hold on;
plot(sunspot(3:315, 1), T, 'g-o');
plot(sunspot(3:315, 1), Ts, 'b-o');
xlabel('Metai');
ylabel('Demiu skaicius');
grid on;
legend('Realus demiu skaicius', ...
    'Prognozuojamas demiu skaicius');
title('Saules demiu prognozavimo patikrinimas 1702-2014 metams');
%12:
e = T - Ts
figure(5);
plot(sunspot(3:315), e, 'r-o');
grid on;
title('Prognozes klaidos grafikas 1702-2014 metams');
xlabel('Metai');
ylabel('Prognozes klaidos reiksmes');
%13:
figure(6);
histogram(e);
title('Prognozes klaidu histograma');
xlabel('Prognozes klaidos reiksme');
ylabel('Daznis');
%14:
mse_reiksme = mse(e)
mad_reiksme = mad(e)
