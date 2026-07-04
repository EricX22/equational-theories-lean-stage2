% order5v2_1852  eq1=536 eq2=61832  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Y,f(Z,f(W,U)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(f(X,X),Y) = f(f(f(Z,X),Y),Z) )).
