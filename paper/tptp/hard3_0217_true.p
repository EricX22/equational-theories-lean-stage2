% hard3_0217  eq1=2049 eq2=215  gold=False
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( X = f(f(f(X,X),Y),f(Z,W)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(X,f(Y,Z)),Y) )).
