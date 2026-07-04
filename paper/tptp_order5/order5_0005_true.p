% order5_0005  eq1=37731 eq2=4884  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(f(f(Y,f(Z,f(Y,X))),Y),Y) )).
fof(goal, conjecture, ! [W,X,Y,Z] : ( X = f(X,f(Y,f(Z,f(W,f(Z,Z))))) )).
