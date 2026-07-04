% order5_0106  eq1=52321 eq2=12315  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( f(X,Y) = f(f(f(X,f(Y,Z)),Z),X) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(Y,f(f(f(Z,Y),Y),f(Y,Y))) )).
