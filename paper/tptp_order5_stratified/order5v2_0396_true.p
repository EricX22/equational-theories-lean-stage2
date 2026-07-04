% order5v2_0396  eq1=34163 eq2=54698  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,Z),f(X,f(Y,Y))),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,f(X,X)) = f(X,f(f(Y,Z),W)) )).
