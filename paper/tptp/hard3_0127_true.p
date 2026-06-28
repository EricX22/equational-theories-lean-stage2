% hard3_0127  eq1=1014 eq2=4158  gold=True
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(f(Z,W),f(U,X))) )).
fof(goal, conjecture, ! [X,Y] : ( f(X,Y) = f(f(f(Y,X),Y),Y) )).
