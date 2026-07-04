% order5v2_0119  eq1=38790 eq2=42653  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(Y,f(f(Z,W),Y)),Y),Z) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(X,f(Y,f(f(X,Z),Y))) )).
