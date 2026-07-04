% order5v2_0341  eq1=30981 eq2=46460  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [U,W,X,Y,Z] : ( X = f(f(Y,f(Z,f(f(W,U),Z))),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( f(X,Y) = f(f(Z,X),f(Z,f(Y,W))) )).
