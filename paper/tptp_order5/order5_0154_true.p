% order5_0154  eq1=43283 eq2=52835  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X] : ( f(X,X) = f(X,f(f(X,X),f(X,X))) )).
fof(goal, conjecture, ! [U,W,X,Y,Z] : ( f(X,Y) = f(f(f(Z,f(W,Y)),U),X) )).
