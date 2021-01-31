clear;
names = {''; 'Efficiency STD'; 'EU tax'; 'Neighbor influence'; 'Tax influence'; 'Member trade multiplier';'Benefit distribution'};
y = [-10 0 10 20 30 40];
%% S_i international trade off
%{
max_eff -0.031001 0.101396 1.011500 0.084276
eutax -0.084756 0.103587 1.013602 0.078998
neighbor_influence -0.053559 0.094336 0.946920 0.085497
tax_influence -0.007071 0.098694 1.046804 0.089160
member_trade_multiplier -0.086956 0.096290 1.028393 0.085278
tax_distribution -0.001428 0.098564 0.972470 0.082092
%}
set(0,'defaultTextFontName','Courier')
x = [-0.031001, -0.084756, -0.053559, -0.007071,-0.086956, -0.001428];
err = [0.101396 0.103587 0.094336 0.098694 0.096290 0.098564];
xlabel('Sobol index value');
errorbar(x,y,err,'horizontal','o')
title('Sobol indices with international trade off');
%set(gca,'ytick',[])
grid on
set(gca,'TickLabelInterpreter','latex')
set(gca,'yticklabel',names)
legend('S_i \pm 95% c.i.')
ylim([-20, 50])
xlim([-.25,.2])
print(gcf,'sioff.png','-dpng','-r300'); 
%% S_T international trade off
x = [1.011500, 1.013602, 0.946920, 1.046804,1.028393, 0.972470];
err = [0.084276 0.078998 0.085497 0.089160  0.085278 0.082092];
xlabel('Sobol index value')

errorbar(x,y,err,'horizontal','o')
title('Total Sobol indices with international trade off');
%set(gca,'ytick',[])
grid on
set(gca,'TickLabelInterpreter','latex')
set(gca,'yticklabel',names)
legend('S_T \pm 95% c.i.')
ylim([-20, 50])
xlim([0.8,1.2])
print(gcf,'stoff.png','-dpng','-r300'); 
%% International trade on S_i
%{
Parameter S1 S1_conf ST ST_conf
max_eff -0.018451 0.102873 0.982444 0.090349
eutax -0.096980 0.099008 1.016613 0.087255
neighbor_influence -0.025812 0.094249 0.930558 0.084024
tax_influence -0.022187 0.098421 1.051939 0.090712
member_trade_multiplier -0.087434 0.096178 1.016088 0.090167
tax_distribution 0.000321 0.097576 0.987125 0.089249
%}
x = [ 0.042738, 0.003296, 0.014169, -0.002387, -0.084593, -0.063780];
err = [0.099506 0.095006 0.097931  0.099184 0.095412 0.092081];

errorbar(x,y,err,'horizontal','o')
xlabel('Sobol index value')
title('Sobol indices with international trade on');
%set(gca,'ytick',[])
grid on
set(gca,'TickLabelInterpreter','latex')
set(gca,'yticklabel',names)
legend('S_i \pm 95% c.i.')
ylim([-20, 50])
xlim([-.25,.2])
print(gcf,'sion.png','-dpng','-r300'); 
%% S_T with international trade on


x = [ 1.021028, 0.950700, 1.008406, 1.002462, 1.027182, 0.992708];
err = [0.081714 0.077230 0.086562  0.078061 0.084182 0.083460];

errorbar(x,y,err,'horizontal','o')
title('Sobol indices with international trade on');
%set(gca,'ytick',[])
grid on
set(gca,'TickLabelInterpreter','latex')
set(gca,'yticklabel',names)
legend('S_T \pm 95% c.i.')
xlabel('Sobol index value')
ylim([-20, 50])
xlim([0.8,1.2])
print(gcf,'ston.png','-dpng','-r300'); 