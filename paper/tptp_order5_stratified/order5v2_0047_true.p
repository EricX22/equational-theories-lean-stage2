% order5v2_0047  eq1=4979 eq2=54735  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(Y,f(X,f(Z,f(X,f(Y,W))))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,f(X,X)) = f(Y,f(f(Z,W),U)) )).
