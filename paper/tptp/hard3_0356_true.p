% hard3_0356  eq1=3380 eq2=4171  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(Z,f(X,f(X,Y))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(f(Y,Y),Z),Y) )).
