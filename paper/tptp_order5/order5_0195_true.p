% order5_0195  eq1=49605 eq2=11771  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [W,X,Y,Z] : ( f(X,X) = f(f(Y,f(Z,f(W,Y))),Y) )).
fof(goal, conjecture, ! [X,Y,Z] : ( X = f(X,f(f(f(Y,X),X),f(Z,Z))) )).
