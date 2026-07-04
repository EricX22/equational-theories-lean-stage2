% order5_0206  eq1=59876 eq2=99  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( f(f(X,Y),Z) = f(W,f(f(Z,W),U)) )).
fof(goal, conjecture, ! [X] : ( X = f(X,f(f(X,X),X)) )).
