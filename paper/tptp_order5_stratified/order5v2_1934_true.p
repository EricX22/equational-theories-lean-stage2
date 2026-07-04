% order5v2_1934  eq1=32340 eq2=23644  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(Y,f(f(Y,f(Z,Y)),W)),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(Y,Z),X),f(Y,f(Z,Z))) )).
