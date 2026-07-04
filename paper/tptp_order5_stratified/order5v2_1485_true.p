% order5v2_1485  eq1=10426 eq2=10024  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(f(Y,Z),f(f(Z,Y),W))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(Y,X),f(f(Y,Y),Z))) )).
