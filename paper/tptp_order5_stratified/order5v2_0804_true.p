% order5v2_0804  eq1=29215 eq2=23166  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(f(f(Y,Z),W),U),f(X,Y)) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(f(f(X,Y),X),f(X,f(X,Z))) )).
