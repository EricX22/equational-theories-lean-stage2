% order5v2_0836  eq1=10209 eq2=44247  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(X,Y),f(f(Y,X),Z))) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,X) = f(Y,f(f(X,f(Z,W)),W)) )).
