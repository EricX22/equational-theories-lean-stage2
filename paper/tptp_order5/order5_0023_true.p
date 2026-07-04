% order5_0023  eq1=12164 eq2=4721  gold=None
% TRUE-direction: prove eq1 |= eq2
fof(hyp,  axiom,      ! [X,Y,Z] : ( X = f(Y,f(f(f(Y,Z),Y),f(Z,X))) )).
fof(goal, conjecture, ! [X,Y] : ( X = f(X,f(X,f(Y,f(Y,f(X,Y))))) )).
