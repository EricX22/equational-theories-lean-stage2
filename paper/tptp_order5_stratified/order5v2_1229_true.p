% order5v2_1229  eq1=23812 eq2=393  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,Z),Z),f(Z,f(Y,W))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Y,Z),W) )).
