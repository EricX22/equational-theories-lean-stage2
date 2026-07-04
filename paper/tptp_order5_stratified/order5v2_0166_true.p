% order5v2_0166  eq1=7207 eq2=47170  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(Y,f(Z,f(f(W,X),f(U,Z)))) )).
fof(goal, conjecture, ! [X,Y,Z] : ( f(X,Y) = f(f(Y,X),f(f(Z,Y),Y)) )).
